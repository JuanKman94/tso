# Temas Selectos de Optimización
Los aspectos a ponderar en el proyecto son:

1. Generador de instancias aleatorias (Random Instance Generator)
2. Heurística que encuentre solución factible a instancia
3. Busqueda local a partir cota obtenida por heurística

Un buen escenario para pruebas se genera con:

```bash
$ ./rig.py 12 10 1500-2000 5000 75-100 10
$ for i in $(seq 1 10); do ./heur.py cflp_12_10_5000-$i.dat; echo "============"; done
```
