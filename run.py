from app import create_app
app = create_app()

if __name__ == "__main__":
    print("Iniciando sistema_biblioteca_mark em modo local...")
    app.run(debug=True)
