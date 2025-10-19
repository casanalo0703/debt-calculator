.PHONY: clean build sign all

# Variables
APP_NAME = "Calculadora de Deudas"
DIST_DIR = dist
BUILD_DIR = build
APP_PATH = "$(DIST_DIR)/$(APP_NAME).app"
EXECUTABLE = "$(APP_PATH)/Contents/MacOS/$(APP_NAME)"

all: build sign

install-deps:
	@echo "📦 Instalando dependencias..."
	@pip install -r requirements.txt

run-dev:
	@echo "🚀 Ejecutando en modo desarrollo..."
	@python src/main.py

build:
	@echo "🏗️  Construyendo aplicación..."
	@pyinstaller src/main.py \
		--name=$(APP_NAME) \
		--windowed \
		--icon=resources/icons/wallet.icns \
		--add-data=resources:resources \
		--add-data=src:. \
		--onedir \
		--clean \
		--noconsole

sign:
	@echo "📝 Dando permisos y firmando la aplicación..."
	@chmod +x $(EXECUTABLE)
	@codesign --force --deep --sign - $(APP_PATH)
	@echo "✅ Construcción completada!"

run:
	@echo "🚀 Ejecutando la aplicación..."
	@open $(APP_PATH)

release-mac:
	@echo "🚀 Construyendo release para macOS..."
	@make clean
	@make build
	@cd dist && zip -r "Calculadora_de_Deudas_macOS.zip" "Calculadora de Deudas.app"
	@echo "✅ Release para macOS completado!"