def writeFile(field, indexType, fileType, data):
    path = 'Indexer/Files/Inverted/' + indexType + fileType
    os.makedirs(path, exist_ok=True)
    with open(path + field, 'w') as f:
        f.write(json.dumps(data))
    
    path = 'Indexer/Files/Inverted/' + indexType + 'Variant/' + fileType
    os.makedirs(path, exist_ok=True)
    with open(path + field, 'wb') as f:
        pickle.dump(encode.encoder(data), f)

    path = 'Indexer/Files/Inverted/' + indexType + 'Pickled/' + fileType
    os.makedirs(path, exist_ok=True)
    with open(path + field, 'wb') as f:
        pickle.dump(data, f)