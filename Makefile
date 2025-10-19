.PHONY: clean build sign all

# Variables
APP_NAME = "Calculadora de Deudas"
DIST_DIR = dist
BUILD_DIR = build
APP_PATH = "$(DIST_DIR)/$(APP_NAME).app"
EXECUTABLE = "$(APP_PATH)/Contents/MacOS/$(APP_NAME)"

all: release-mac

clean:
	@echo "🧹 Limpiando directorios anteriores..."
	@rm -rf $(BUILD_DIR) $(DIST_DIR)
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete

install-deps:
	@echo "📦 Instalando dependencias..."
	@pip install -r requirements.txt

run-dev:
	@echo "🚀 Ejecutando en modo desarrollo..."
	@python src/main.py

build: clean
	@echo "🏗️  Construyendo aplicación..."
	@pyinstaller calculadora_de_deudas.spec --clean --noconfirm

run:
	@echo "🚀 Ejecutando la aplicación..."
	@open $(APP_PATH)

release-mac: clean build
	@echo "🚀 Construyendo release para macOS..."
	@cd dist && zip -r "Calculadora_de_Deudas_macOS.zip" "Calculadora de Deudas.app"
	@echo "✅ Release para macOS completado!"