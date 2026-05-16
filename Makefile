.PHONY: clean build sign build-windows all

# Variables
APP_NAME = Calculadora de Deudas
DIST_DIR = dist
BUILD_DIR = build
APP_PATH = $(DIST_DIR)/$(APP_NAME).app
EXECUTABLE = $(APP_PATH)/Contents/MacOS/$(APP_NAME)

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
	export ENV=dev && python src/main.py

build: clean
	@echo "🏗️  Construyendo aplicación..."
	@pyinstaller calculadora_de_deudas.spec --clean --noconfirm

sign:
	@echo "📝 Dando permisos y firmando la aplicación..."
	@chmod +x "$(EXECUTABLE)"
	@codesign --force --deep --sign - "$(APP_PATH)"
	@echo "✅ Aplicación firmada!"

run:
	@echo "🚀 Ejecutando la aplicación..."
	@open "$(APP_PATH)"

release-mac: build sign
	@echo "📦 Creando archivo comprimido..."
	@cd "$(DIST_DIR)" && zip -r "Calculadora_de_Deudas_macOS.zip" "$(APP_NAME).app"
	@echo "✅ Release para macOS completado!"

# ===== Targets para Windows =====

WINDOWS_APP_NAME = Calculadora de Deudas
WINDOWS_DIST = $(DIST_DIR)/$(WINDOWS_APP_NAME)

build-windows: clean
	@echo "🏗️  Construyendo aplicación para Windows..."
	@pyinstaller calculadora_de_deudas_windows.spec --clean --noconfirm

release-windows: build-windows
	@echo "📦 Creando archivo comprimido para Windows..."
	@cd "$(DIST_DIR)" && powershell -Command "if (Test-Path '$(WINDOWS_APP_NAME)') { Compress-Archive -Path '$(WINDOWS_APP_NAME)' -DestinationPath 'Calculadora_de_Deudas_Windows.zip' -Force; Write-Host 'Compresión completada!' }"
	@echo "✅ Release para Windows completado!"

# Alternativa con 7zip si está disponible
release-windows-7z: build-windows
	@echo "📦 Creando archivo 7z para Windows..."
	@7z a "$(DIST_DIR)/Calculadora_de_Deudas_Windows.7z" "$(WINDOWS_DIST)"
	@echo "✅ Release para Windows (7z) completado!"

# ===== Targets para Linux =====

LINUX_APP_NAME = Calculadora de Deudas
LINUX_DIST = $(DIST_DIR)/$(LINUX_APP_NAME)

build-linux: clean
	@echo "🏗️  Construyendo aplicación para Linux..."
	@pyinstaller calculadora_de_deudas_linux.spec --clean --noconfirm

release-linux: build-linux
	@echo "📦 Creando archivo comprimido para Linux..."
	@cd "$(DIST_DIR)" && tar -czf "Calculadora_de_Deudas_Linux.tar.gz" "$(LINUX_APP_NAME)"
	@echo "✅ Release para Linux completado!"