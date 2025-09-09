#!/bin/bash

set -eo pipefail

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="reporte_uso_real_${TIMESTAMP}.csv"

if [ "$EUID" -ne 0 ]; then
    echo "Error: Este script debe ejecutarse con privilegios de administrador (sudo)."
    exit 1
fi

for cmd in virsh xmllint pgrep awk ps du sort; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "Error: El comando requerido '$cmd' no está instalado."
        exit 1
    fi
done

echo "[🚀] Generando reporte en archivo CSV..."
echo "[⏳] Esto tardará 1 segundo por cada VM activa..."

JIFFIES_PER_SEC=$(getconf CLK_TCK)
REPORT_LINES=()

RUNNING_VMS=$(virsh list --state-running --name | grep 'instance-' || true)

if [ -z "$RUNNING_VMS" ]; then
    echo "No se encontraron instancias de OpenStack en ejecución. No se generó ningún reporte."
    exit 0
fi

while IFS= read -r instance; do
    XML_DATA=$(virsh dumpxml "$instance")
    UUID=$(echo "$XML_DATA" | xmllint --xpath 'string(/domain/uuid)' - 2>/dev/null)
    if [ -z "$UUID" ]; then continue; fi

    PID=$(pgrep -f "qemu-system-x86.*$UUID" | head -n 1 || true)
    if [ -z "$PID" ] || [ ! -d "/proc/$PID" ]; then continue; fi

    PROJECT=$(echo "$XML_DATA" | xmllint --xpath "string(//*[local-name()='project'])" - 2>/dev/null)
    FLAVOR=$(echo "$XML_DATA" | xmllint --xpath "string(//*[local-name()='flavor']/@name)" - 2>/dev/null)
    PROJECT=${PROJECT:-"N/A"}
    FLAVOR=${FLAVOR:-"N/A"}

    read -r _ _ _ _ _ _ _ _ _ _ _ _ _ utime stime _ < "/proc/$PID/stat"
    prev_cpu_time=$((utime + stime))
    sleep 1
    read -r _ _ _ _ _ _ _ _ _ _ _ _ _ utime stime _ < "/proc/$PID/stat"
    curr_cpu_time=$((utime + stime))
    delta_cpu=$((curr_cpu_time - prev_cpu_time))
    cpu_percent=$(awk "BEGIN {printf \"%.2f\", ($delta_cpu / $JIFFIES_PER_SEC) * 100}")

    mem_kb=$(ps -p "$PID" -o rss= --no-headers)
    mem_mb=$((mem_kb / 1024))

    total_disk_gb_vm=0
    disk_paths=$(echo "$XML_DATA" | xmllint --xpath '//disk[@device="disk"]/source/@file' - 2>/dev/null | sed 's/ file="\([^"]*\)"/\1/g')
    for d_path in $disk_paths; do
        if [ -f "$d_path" ]; then
            disk_kb_file=$(du -k "$d_path" | awk '{print $1}')
            total_disk_gb_vm=$(awk "BEGIN {print $total_disk_gb_vm + ($disk_kb_file / 1024 / 1024)}")
        fi
    done
    disk_gb=$(printf "%.2f" "$total_disk_gb_vm")

    REPORT_LINES+=("${PROJECT}|${instance}|${FLAVOR}|${cpu_percent}|${mem_mb}|${disk_gb}")

done <<< "$RUNNING_VMS"

echo "PROYECTO,ID DE INSTANCIA,FLAVOR,CPU REAL (%),MEMORIA REAL (MB),DISCO REAL (GB)" > "$OUTPUT_FILE"
printf "%s\n" "${REPORT_LINES[@]}" | sort -t'|' -k1 | sed 's/|/,/g' >> "$OUTPUT_FILE"

echo ""
echo -e "[✅] Reporte guardado exitosamente en el archivo: ${OUTPUT_FILE}"
