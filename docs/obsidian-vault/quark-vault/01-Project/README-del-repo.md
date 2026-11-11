---
title: "README del repositorio"
tags: [proyecto]
source: README.md
status: snapshot
---

# Quark Anticheat: sistema anticheat nativo para GNU/Linux

Prototipo funcional de un sistema anticheat nativo de nivel de kernel (Ring 0) diseñado específicamente para distribuciones GNU/Linux. El proyecto analiza y demuestra la viabilidad técnica de interceptar y prevenir vectores de ataque comunes en videojuegos multijugador competitivos sin comprometer la estabilidad del sistema ni la experiencia del usuario.

## Componentes del sistema

El sistema está estructurado en tres elementos principales que operan de forma coordinada:
* **Módulo de kernel**: desarrollado en C, se encarga de la supervisión de accesos a la memoria de los procesos protegidos mediante **kretprobes**, interceptando el retorno de `ptrace_may_access()` para denegar los accesos externos.
* **Servicio en espacio de usuario**: actúa como un demonio (daemon) que gestiona la comunicación bidireccional con el kernel a través de un socket `netlink` y de un socket de dominio Unix, procesa los eventos de seguridad y aplica las políticas de mitigación.
* **Interfaz de integración (API/SDK)**: biblioteca orientada a desarrolladores que permite acoplar las capacidades de supervisión del anticheat en videojuegos de código abierto de manera flexible.

## Tecnologías y herramientas clave

* **Lenguajes de programación**: C (módulo de kernel y SDK) y Rust (demonio de espacio de usuario, sin dependencias externas).
* **Mecanismos de mediación del kernel**: kretprobes sobre `ptrace_may_access()`, con sobrescritura del valor de retorno para denegar el acceso.
* **Comunicación interna**: socket netlink (protocolo 31) entre el demonio y el módulo, y socket de dominio Unix entre el SDK y el demonio.
* **Entorno de referencia**: Nobara Linux (distribución optimizada para gaming basada en Fedora).
* **Aislamiento y pruebas**: virtualización avanzada mediante QEMU/KVM para la ejecución segura y el debugging de código con privilegios elevados.

## Estructura del repositorio

El repositorio se organiza bajo una arquitectura modular de monorepo:
* `/kernel`: código fuente en C del módulo de kernel (kretprobe sobre `ptrace_may_access()` y socket netlink).
* `/quark_daemon`: demonio de espacio de usuario en Rust, más el cliente netlink auxiliar `quark_cli` (C).
* `/sdk`: biblioteca C de integración (`quark_sdk.h` / `quark_sdk.c`) que el videojuego enlaza.
* `/game_target`: videojuego *mock* en C usado como objetivo de prueba.
* `/cheat`: herramienta de ataque en C que escribe sobre `/proc/<PID>/mem`.
* `/tooling`: entorno de compilación en contenedor para RecoilEngine (Fedora 44, glibc de la VM de pruebas).
* `/docs`: documentación técnica y registro del entorno de validación.
* Los scripts de validación (`run_test.sh`, `run_test_no_quark.sh`, `run_test_kernel.sh`) están en la raíz del repositorio.

## Requisitos previos

Para configurar el entorno de desarrollo y compilación se requiere:
* cabeceras del kernel en ejecución (`kernel-devel`) y soporte de kprobes/kretprobes (`CONFIG_KPROBES`).
* herramientas de compilación C (`make`, `gcc`).
* cadena de herramientas de Rust estable (`cargo`) para el demonio de espacio de usuario.
* privilegios de `root` para cargar el módulo (`insmod`), preferentemente dentro de una máquina virtual QEMU/KVM.

## Autores

Proyecto desarrollado como Proyecto Integrador Final (PIF) en la carrera de Ingeniería en Sistemas de Información de la Universidad de la Cuenca del Plata:
* Martínez Alarcón, Gabriel Sebastián
* Merino De Rui, Stefano Nahuel


## Update 2026-11-11 — agent:claude
Snapshot del README **local sin commitear**. El README de `origin/Dev` es la versión aspiracional anterior (Rust, LSM, `/userspace`, `/tests` que no existen). Ver [[Contexto-del-proyecto]] Update 2026-11-11.
