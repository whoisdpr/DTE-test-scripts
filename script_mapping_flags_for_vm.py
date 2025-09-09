#!/usr/bin/env python3
import pandas as pd
from io import StringIO
import subprocess

# ==== Configuración ====
vm_name = "VM1"  # Cambiar por el nombre de la VM si se desea
vm_flags_file = "vm_flags.txt"

# ==== CSVs incrustados ====
dc_stg1_csv = """Device,Categoría,Flag,Descripción
DC-STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,mmx,Extensiones SIMD para procesamiento paralelo
DC-STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,sse,Extensiones SIMD para procesamiento paralelo
DC-STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,sse2,Extensiones SIMD para procesamiento paralelo
DC-STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,ssse3,Extensiones SIMD para procesamiento paralelo
DC-STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,sse4_1,Extensiones SIMD para procesamiento paralelo
DC-STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,sse4_2,Extensiones SIMD para procesamiento paralelo
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx2,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512f,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512bw,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512cd,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512dq,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512vl,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512ifma,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512vbmi,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512_vbmi2,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512_vnni,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512_bitalg,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512_fp16,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,avx512_bf16,Variantes de AVX y AVX-512 para cómputos vectoriales
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,f16c,Conversión entre float de 16 y 32 bits
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,fma,Fused Multiply-Add (mayor precisión y rendimiento)
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,3dnowprefetch,Optimización de acceso a memoria
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,gfni,Instrucciones avanzadas vectoriales para criptografía
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,vaes,Instrucciones avanzadas vectoriales para criptografía
DC–STG1,Instrucciones SIMD y Extensiones de Procesamiento Vectorial,vpclmulqdq,Instrucciones avanzadas vectoriales para multiplicación
DC–STG1,Seguridad y Mitigaciones,nx,Protección contra ejecución de código en datos (No-eXecute bit)
DC–STG1,Seguridad y Mitigaciones,smep,Prevención de ejecución desde user space al kernel
DC–STG1,Seguridad y Mitigaciones,smap,Prevención de acceso desde user space al kernel
DC–STG1,Seguridad y Mitigaciones,ssbd,Mitigaciones contra vulnerabilidades tipo Spectre/Meltdown
DC–STG1,Seguridad y Mitigaciones,ibrs,Mitigaciones contra vulnerabilidades tipo Spectre/Meltdown
DC–STG1,Seguridad y Mitigaciones,ibpb,Mitigaciones contra vulnerabilidades tipo Spectre/Meltdown
DC–STG1,Seguridad y Mitigaciones,stibp,Mitigaciones contra vulnerabilidades tipo Spectre/Meltdown
DC–STG1,Seguridad y Mitigaciones,ibrs_enhanced,Mitigaciones contra vulnerabilidades tipo Spectre/Meltdown
DC–STG1,Seguridad y Mitigaciones,md_clear,Borrado de registros para mitigar ataques de canal lateral
DC–STG1,Seguridad y Mitigaciones,serialize,Serialización para mitigar ataques de canal lateral
DC–STG1,Seguridad y Mitigaciones,tsxldtrk,Nuevas mitigaciones y configuraciones de seguridad
DC–STG1,Seguridad y Mitigaciones,pconfig,Nuevas mitigaciones y configuraciones de seguridad
DC–STG1,Seguridad y Mitigaciones,arch_capabilities,Nuevas mitigaciones y configuraciones de seguridad
DC–STG1,Seguridad y Mitigaciones,flush_l1d,Nuevas mitigaciones y configuraciones de seguridad
DC–STG1,Seguridad y Mitigaciones,ibt,Indirect Branch Tracking (mitigación Spectre-v2)
DC–STG1,Seguridad y Mitigaciones,umip,Restricción de instrucciones privilegiadas en modo usuario
DC–STG1,Seguridad y Mitigaciones,pku,Restricción de instrucciones privilegiadas en modo usuario
DC–STG1,Seguridad y Mitigaciones,ospke,Restricción de instrucciones privilegiadas en modo usuario
DC–STG1,Seguridad y Mitigaciones,tme,Total Memory Encryption
"""

dc_az1_wn1_csv = """Device,Categoría,Flag,Descripción,Soporte
DC-AZ1-WN1,Virtualización,HYPERVISOR,Indica que el sistema operativo se ejecuta dentro de una máquina virtual o que el procesador soporta virtualización por hardware,Soportado
DC-AZ1-WN1,Virtualización,VMX,Soporte para virtualización asistida por hardware de Intel,Soportado
DC-AZ1-WN1,Virtualización,SVM,Soporte para virtualización asistida por hardware de AMD,No soportado
DC-AZ1-WN1,Gestion de Memoria,PAGE1GB,Soporte para páginas de 1 GB (mejora rendimiento en cargas grandes),Soportado
DC-AZ1-WN1,Gestion de Memoria,PAE,Soporta direcciones físicas de más de 32 bits (útil en sistemas de 32 bits),Soportado
DC-AZ1-WN1,Gestion de Memoria,PAT,Permite configurar atributos de caché por página,Soportado
DC-AZ1-WN1,Gestion de Memoria,PSE,Soporte para páginas de 4 MB (reduce sobrecarga de TLB),Soportado
DC-AZ1-WN1,Gestion de Memoria,PSE36,Extensión de PSE con direcciones físicas de más de 32 bits,Soportado
DC-AZ1-WN1,Gestion de Memoria,NX,Previene ejecución de código en regiones marcadas como datos,Soportado
DC-AZ1-WN1,Gestion de Memoria,SMEP,Previene ejecución de código de usuario en modo kernel,Soportado
DC-AZ1-WN1,Gestion de Memoria,SMAP,Impide acceso de kernel a páginas de usuario,Soportado
DC-AZ1-WN1,SIMD,SSE,Instrucciones para operaciones vectoriales y multimedia,Soportado
DC-AZ1-WN1,SIMD,SSE2,Instrucciones para operaciones vectoriales y multimedia,Soportado
DC-AZ1-WN1,SIMD,SSE3,Instrucciones para operaciones vectoriales y multimedia,Soportado
DC-AZ1-WN1,SIMD,SSE4.1,Instrucciones para operaciones vectoriales y multimedia,Soportado
DC-AZ1-WN1,SIMD,SSE4.2,Instrucciones para operaciones vectoriales y multimedia,Soportado
DC-AZ1-WN1,SIMD,AES,Instrucciones para cifrado AES,Soportado
DC-AZ1-WN1,SIMD,AVX,Extensiones vectoriales avanzadas para datos de mayor ancho,Soportado
DC-AZ1-WN1,SIMD,AVX2,Extensiones vectoriales avanzadas para datos de mayor ancho,Soportado
DC-AZ1-WN1,SIMD,AVX-512-F,Subconjuntos de instrucciones AVX-512,Soportado
DC-AZ1-WN1,SIMD,AVX-512-DQ,Subconjuntos de instrucciones AVX-512,Soportado
DC-AZ1-WN1,SIMD,AVX-512-IFMA,Subconjuntos de instrucciones AVX-512,Soportado
DC-AZ1-WN1,SIMD,AVX-512-CD,Subconjuntos de instrucciones AVX-512,Soportado
DC-AZ1-WN1,SIMD,AVX-512-BW,Subconjuntos de instrucciones AVX-512,Soportado
DC-AZ1-WN1,SIMD,AVX-512-VL,Subconjuntos de instrucciones AVX-512,Soportado
DC-AZ1-WN1,SIMD,FMA,Multiplicación y suma en una sola instrucción,Soportado
DC-AZ1-WN1,Otras Extensiones,CLFSH,Limpieza de líneas de caché,Soportado
DC-AZ1-WN1,Otras Extensiones,BMI1,Extensiones para manipulación eficiente de bits,Soportado
DC-AZ1-WN1,Otras Extensiones,BMI2,Extensiones para manipulación eficiente de bits,Soportado
DC-AZ1-WN1,Otras Extensiones,RDTSC,Lectura precisa del contador de tiempo,Soportado
DC-AZ1-WN1,Otras Extensiones,RDTSCP,Lectura precisa del contador de tiempo,Soportado
DC-AZ1-WN1,Otras Extensiones,TSC-DEADLINE,Mejora de temporización por TSC,Soportado
DC-AZ1-WN1,Otras Extensiones,TSC-INVARIANT,Mejora de temporización por TSC,Soportado
DC-AZ1-WN1,Otras Extensiones,MSR,Acceso y control sobre registros de modelo,Soportado
DC-AZ1-WN1,Otras Extensiones,MTRR,Control sobre políticas de memoria,Soportado
DC-AZ1-WN1,Otras Extensiones,XSAVE,Guardado/restauración del estado extendido,Soportado
DC-AZ1-WN1,Otras Extensiones,OSXSAVE,Guardado/restauración del estado extendido,Soportado
DC-AZ1-WN1,Otras Extensiones,RDRAND,Generación de números aleatorios por hardware,Soportado
DC-AZ1-WN1,Otras Extensiones,RDSEED,Generación de números aleatorios por hardware,Soportado
DC-AZ1-WN1,Otras Extensiones,CMOV,Instrucciones condicionales,Soportado
DC-AZ1-WN1,Otras Extensiones,CX8,Instrucciones atómicas,Soportado
DC-AZ1-WN1,Otras Extensiones,CX16,Instrucciones atómicas,Soportado
DC-AZ1-WN1,Otras Extensiones,ADX,Operaciones aritméticas de precisión extendida,Soportado
DC-AZ1-WN1,Otras Extensiones,F16C,Soporte para números de 16 bits en coma flotante,Soportado
DC-AZ1-WN1,Otras Extensiones,FXSR,Guardado/restauración de estado de coma flotante/MMX,Soportado
DC-AZ1-WN1,Otras Extensiones,MONITOR,Instrucciones para espera eficiente de eventos,Soportado
DC-AZ1-WN1,Otras Extensiones,MOVBE,Soporte para formato big-endian en movimientos,Soportado
DC-AZ1-WN1,Otras Extensiones,ERMSB,REP MOVSB/STOSB mejorado,Soportado
DC-AZ1-WN1,Otras Extensiones,PCLMULDQ,Multiplicación de polinomios (criptografía),Soportado
DC-AZ1-WN1,Otras Extensiones,POPCNT,Conteo de bits,Soportado
DC-AZ1-WN1,Otras Extensiones,LZCNT,Conteo de ceros líderes,Soportado
DC-AZ1-WN1,Otras Extensiones,SEP,Llamadas al sistema rápidas,Soportado
DC-AZ1-WN1,Otras Extensiones,LAHF-SAHF,Transferencia de flags en modo 64 bits,Soportado
DC-AZ1-WN1,Otras Extensiones,HLE,Soporte para memoria transaccional,Soportado
DC-AZ1-WN1,Otras Extensiones,RTM,Soporte para memoria transaccional,Soportado
DC-AZ1-WN1,Otras Extensiones,RDWRFSGSBASE,Acceso directo a segmentos FS y GS,Soportado
DC-AZ1-WN1,Funciones de Seguridad,CET,Protección del flujo de control contra ataques de reutilización,Soportado
DC-AZ1-WN1,Funciones de Seguridad,Kernel CET,CET habilitado para modo kernel,Soportado
DC-AZ1-WN1,Funciones de Seguridad,User CET,CET en modo usuario,No soportado
DC-AZ1-WN1,Funciones de Seguridad,MPX,Extensiones de protección de memoria Intel,No soportado
DC-AZ1-WN1,Funciones de Seguridad,SMX,Intel Trusted Execution,No soportado
DC-AZ1-WN1,Funciones de Seguridad,SKINIT,Inicio confiable AMD,No soportado
DC-AZ1-WN1,Funciones de Seguridad,SGX,Extensiones de enclaves seguros Intel,No soportado
DC-AZ1-WN1,Gestion de Energía y Rendimiento,EIST,Ajuste dinámico de frecuencia y voltaje (Intel Speedstep),Soportado
DC-AZ1-WN1,Gestion de Energía y Rendimiento,ACPI,Interfaz avanzada de configuración y energía,Soportado
DC-AZ1-WN1,Gestion de Energía y Rendimiento,TM,Monitorización térmica y control,Soportado
DC-AZ1-WN1,Gestion de Energía y Rendimiento,TM2,Monitorización térmica y control,Soportado
DC-AZ1-WN1,Gestion de Energía y Rendimiento,APIC,Controlador de interrupciones programable local,Soportado
DC-AZ1-WN1,Gestion de Energía y Rendimiento,x2APIC,Controlador de interrupciones extendido,Soportado
DC-AZ1-WN1,Depuración,DTES64,Rastro de bifurcaciones de 64 bits,Soportado
DC-AZ1-WN1,Depuración,DS-CPL,Depuración por nivel de privilegio,No soportado
DC-AZ1-WN1,Depuración,PCID,Identificadores de contexto de proceso (mejora TLB),Soportado
DC-AZ1-WN1,Depuración,INPCID,Identificadores de contexto de proceso (mejora TLB),Soportado
DC-AZ1-WN1,Depuración,PDCM,Capacidad de rendimiento en MSR,Soportado
DC-AZ1-WN1,Depuración,xTPR,Control de prioridad de tareas,Soportado
DC-AZ1-WN1,Flags Misceláneas,PGE,Entradas globales en tablas de páginas,Soportado
DC-AZ1-WN1,Flags Misceláneas,SS,Snooping del bus para coherencia de caché,Soportado
DC-AZ1-WN1,Flags Misceláneas,VME,Modo virtual 8086,Soportado
DC-AZ1-WN1,Flags Misceláneas,DCA,Acceso directo a caché desde dispositivos,No soportado
DC-AZ1-WN1,Flags Misceláneas,FFXSR,Versión optimizada de FXSAVE/FXRSTOR,No soportado
DC-AZ1-WN1,Flags Misceláneas,CNXT-ID,Modo adaptativo de caché L1 o configurado por BIOS,No soportado
DC-AZ1-WN1,Flags Misceláneas,MCE,Mecanismos de detección de errores de hardware,Soportado
DC-AZ1-WN1,Flags Misceláneas,MCA,Manejo de errores de hardware,Soportado
DC-AZ1-WN1,Flags Misceláneas,PBE,Pin para errores de paridad del bus,Soportado
DC-AZ1-WN1,Flags Misceláneas,PSN,Número de serie de procesador,No soportado
DC-AZ1-WN1,Flags Misceláneas,PREFETCHW,Precarga de caché para escritura,Soportado
"""

# ==== Leer los CSV desde strings ====
df_stg1 = pd.read_csv(StringIO(dc_stg1_csv))
df_stg1['Flag'] = df_stg1['Flag'].astype(str).str.lower()
df_stg1['ServerFile'] = 'dc-stg1'

df_az1 = pd.read_csv(StringIO(dc_az1_wn1_csv))
df_az1['Flag'] = df_az1['Flag'].astype(str).str.lower()
df_az1['ServerFile'] = 'dc-az1-wn1'

# Concatenar todos los flags de servidores
server_flags_df = pd.concat([df_stg1, df_az1], ignore_index=True)

# ==== Extraer flags de la VM ====
subprocess.run(f"cat /proc/cpuinfo | grep -m1 'flags' | cut -d: -f2 | tr -s ' ' '\n' | sort -u > {vm_flags_file}", shell=True)
with open(vm_flags_file, "r") as f:
    vm_flags = set([line.strip().lower() for line in f if line.strip()])

# ==== Comparación ====
match_df = server_flags_df[server_flags_df['Flag'].isin(vm_flags)].copy()
match_df['VM'] = vm_name
match_df = match_df[['VM', 'Flag', 'Categoría', 'Descripción', 'ServerFile']]

missing_df = server_flags_df[~server_flags_df['Flag'].isin(vm_flags)].copy()
missing_df['VM'] = vm_name
missing_df = missing_df[['VM', 'Flag', 'Categoría', 'Descripción', 'ServerFile']]

# ==== Guardar reportes ====
match_df.to_csv("reporte_coinciden.csv", index=False)
missing_df.to_csv("reporte_faltan.csv", index=False)

print("Reportes generados: reporte_coinciden.csv y reporte_faltan.csv")
