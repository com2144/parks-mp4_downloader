from action_handler import ActionHandler

class DownLoadModel:
    def __init__(self, argv):
        self.path = ''
        self.action = ActionHandler(argv)

        # test
        self.path = '/home/west/바탕화면/test'

    def download_url_file(self):
        version_fields = ["id", "sg_uploaded_movie"]
        for sid in self.action.selected_ids_filter:
            version = self.action.sg.find_one(self.action.entity_type, [sid], version_fields)
            mp4_down = self.path + '/' + version["sg_uploaded_movie"]["name"]
            mp4_filter = mp4_down.split('.')
            low_ext = mp4_filter[-1].lower()
            if low_ext != 'mp4':
                pass
            else:
                self.action.sg.download_attachment(version["sg_uploaded_movie"], file_path=mp4_down)
def main():


if __name__ == '__main__':
    main()