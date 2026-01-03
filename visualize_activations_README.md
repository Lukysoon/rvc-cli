# RVC Model Activation Comparison

Notebook pro porovnání aktivací dvou RVC modelů a selektivní kopírování vah.

## Co to dělá

1. Načte dva RVC modely
2. Pustí stejné audio přes oba modely
3. Zachytí aktivace (výstupy) všech vrstev
4. Najde vrstvy s největšími rozdíly
5. Zkopíruje váhy těchto vrstev z jednoho modelu do druhého
6. Uloží hybridní model

## Konfigurace

```python
MODEL_PATH_1 = "model_source.pth"  # Zdrojový model (odkud kopírovat)
MODEL_PATH_2 = "model_target.pth"  # Cílový model (kam kopírovat)
AUDIO_PATH = "audio.wav"           # Audio pro analýzu
TOP_SCALARS = 10000                # Počet skalárních rozdílů k analýze
TOP_N_LAYERS = 10                  # Počet vrstev ke kopírování
```

## Parametry

### TOP_SCALARS
Kolik největších skalárních rozdílů v aktivacích analyzovat.

| Hodnota | Pokrytí vrstev | Rychlost |
|---------|----------------|----------|
| 1,000 | ~10-20 vrstev | Rychlé |
| 10,000 | ~50-100 vrstev | Doporučeno |
| 100,000 | ~200+ vrstev | Pomalé |

### TOP_N_LAYERS
Kolik vrstev s největšími rozdíly zkopírovat.

| Hodnota | Efekt |
|---------|-------|
| 3-5 | Jemná změna |
| 10-15 | Střední změna |
| 20+ | Výrazná změna |

## Jak to funguje

### 1. Aktivace
Aktivace = výstup vrstvy při průchodu dat modelem.

```
Input audio
    ↓
┌─────────────┐
│   enc_p     │ → aktivace: tensor [1, 768, 308]
└─────────────┘
    ↓
┌─────────────┐
│   flow      │ → aktivace: tensor [1, 192, 308]
└─────────────┘
    ↓
Output audio
```

### 2. Porovnání
Pro každou vrstvu: `diff = |aktivace_model1 - aktivace_model2|`

### 3. Výběr vrstev
1. Najdi TOP_SCALARS největších rozdílů (skalárů)
2. Spočítej, kolik skalárů pochází z které vrstvy
3. Vyber TOP_N_LAYERS vrstev s nejvíce rozdíly

### 4. Kopírování vah
Pro každou vybranou vrstvu zkopíruj všechny její váhy:
- `layer.weight`
- `layer.bias`
- (a další parametry)

## Struktura RVC modelu

```
Synthesizer (433 submodulů, 457 weight tensorů)
├── enc_p          # TextEncoder - zpracování phone/pitch
│   ├── emb_phone
│   ├── emb_pitch
│   └── encoder
│       └── attn_layers.0-5
├── dec            # Generator - generování audia
│   ├── conv_pre
│   ├── ups.0-3
│   ├── resblocks.0-11
│   └── conv_post
├── flow           # ResidualCouplingBlock
│   └── flows.0-3
└── emb_g          # Speaker embedding
```

## Úrovně granularity

| Úroveň | Popis | Počet |
|--------|-------|-------|
| Modul | enc_p, dec, flow | ~5 |
| Submodul | Všechny vrstvy | 433 |
| Weight tensor | Jednotlivé váhové matice | 457 |
| Skalár aktivace | Hodnoty v aktivacích | miliony |

## Příklad výstupu

```
Top 5 vrstev ke kopírování:
  dec.resblocks.1: 450 skalárů (45%)
  enc_p.encoder.attn_layers.0: 200 skalárů (20%)
  dec.resblocks.2: 150 skalárů (15%)
  dec.conv_pre: 100 skalárů (10%)
  flow.flows.0: 50 skalárů (5%)

Zkopírováno 35 weight tensorů
```

## Požadavky

- PyTorch
- librosa
- matplotlib
- RVC-CLI projekt (pro Synthesizer a load_embedding)
