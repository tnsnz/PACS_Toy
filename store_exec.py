# def main(args):
#     if args is not None:
#         sys.argv = args
#
#     args = _setup_argparser()
#
#     a = QApplication(sys.argv)
#     is_dir = True
#
#     if is_dir:
#         selected_files = [QFileDialog.getExistingDirectory(
#             None,
#             "Select Directory",
#             ""
#         )]
#     else:
#         selected_files = QFileDialog.getOpenFileNames(
#             None,
#             "Select Files",
#             ""
#         )[0]
#
#     scu = StoreSCU(is_dir)
#     scu.request(args, selected_files)
#     a.exec()
#
#
# if __name__ == '__main__':
#     main(['moc_scu.py', 'localhost', '11112', r'C:\Users\tndns\Desktop\workspace\origin\PACS_Toy\app\store_dir'])