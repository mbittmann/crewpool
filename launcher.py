import inference


model_path = 'model/model.h5'

def main():
    model = inference.load_model(model_path)

if __name__ == "__main__":
    main()