# Installation

## Gereksinimler

- Python 3.10 veya üzeri
- Git
- OpenRouter API anahtarı

## Adım 1: Depoyu Klonlayın

```bash
git clone https://github.com/sizin-kullanici-adiniz/market-gap-analyzer.git
cd market-gap-analyzer
```

## Adım 2: Sanal Ortam Oluşturun

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

## Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

## Adım 4: Projeyi Doğrulayın

```bash
python main.py --help
```

Bu komut, CLI arayüzünün doğru şekilde yüklendiğini ve çalışma ortamının hazır olduğunu gösterir.

## OpenRouter Notu

Kurulumdan sonra `.env` dosyasında `OPENROUTER_API_KEY` ve tercih ettiğiniz `OPENROUTER_MODEL` değerini tanımlayın. OpenRouter ücretsiz modellerini kullanacaksanız model adının `:free` ile bittiğini doğrulayın.
