# Installation

## Gereksinimler

- Python 3.10 veya üzeri
- Git
- OpenRouter API anahtarı veya DeepSeek API anahtarı

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

## Sağlayıcı Notu

Kurulumdan sonra `.env` dosyasında seçtiğiniz sağlayıcı için gerekli değişkenleri tanımlayın. OpenRouter kullanacaksanız `OPENROUTER_API_KEY` ve `OPENROUTER_MODEL` değerlerini girin. DeepSeek kullanacaksanız `LLM_PROVIDER=deepseek`, `DEEPSEEK_API_KEY` ve tercihen `DEEPSEEK_MODEL=deepseek-v4-flash` tanımlayın. DeepSeek'te daha iyi analiz kalitesi için düşünme modu varsayılan olarak açıktır; gerekirse `DEEPSEEK_THINKING_ENABLED=false` ile kapatabilirsiniz.
