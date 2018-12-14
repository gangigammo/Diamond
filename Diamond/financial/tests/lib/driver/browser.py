
# ブラウザの定義


class Browser():
    def __init__(self, name, bin_path, factory_method, download_url):
        self.name = name
        self.bin_path = bin_path
        self.factory_method = factory_method
        self.download_url = download_url
