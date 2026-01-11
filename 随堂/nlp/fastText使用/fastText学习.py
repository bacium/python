import fasttext


def train_model(train_file):
    model = fasttext.train_supervised(input=train_file,
                                      lr=0.1,
                                      epoch=10,
                                      wordNgrams=2,
                                      minCount=1,
                                      verbose=2)
    # model.save_model(model_file)
    print(model)


if __name__ == '__main__':
    train_model('./data/cooking.pre.train')
