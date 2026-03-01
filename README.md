## Comandos

### Desarrollo

```bash
pip install -e .
./scripts/start_dev.sh
```

Alternativa directa:

```bash
PYTHONPATH=src uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Produccion

```bash
./scripts/start_prod.sh
```

### Docker Compose

```bash
docker compose -f compose.yaml up --build
```

### Tests

```bash
python -m pytest -q
```
