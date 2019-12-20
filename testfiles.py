import sys
import time
from threading import Thread

import wx

total_progress = 0
total_value = 0


class TestPanel(wx.Panel):
    def __init__(self, frame: wx.Frame):
        import sys

        wx.Panel.__init__(self, frame, pos=(0, 0), size=(624, 648))

        self.index = 0
        self.currentItem = None

        self.log = wx.TextCtrl(self, id=wx.ID_ANY, pos=(8, 8), size=(300, 600), style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_LEFT|wx.TE_RICH|wx.TE_READONLY)
        self.progress = wx.Gauge(self, id=wx.ID_ANY, pos=(8, 616), size=(300, 24))

        self.test_list = wx.ListCtrl(self, pos=(316, 8), size=(200, 600), style=wx.LC_REPORT|wx.BORDER_SUNKEN|wx.LC_SINGLE_SEL)
        # self.test_list.SetItemCount(2)
        self.test_list.InsertColumn(0, "Test", width=300)
        # self.seedintTest = wx.ListItem()
        # self.seedintTest.SetText("Seedint Test")
        # self.test_list.Update()
        # self.test_list.InsertItem(0, "Seedint Test")

        self.add_line("Seedint Test")
        self.add_line("Offset File")

        self.test_btn = wx.Button(self, id=wx.ID_ANY, pos=(456, 615), size=(60, -1), label="TEST!")
        self.test_btn.Bind(wx.EVT_BUTTON, self.test, id=wx.ID_ANY)

        self.test_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.test_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeselected)

        sys.stderr = self
        sys.stdout = self

        Thread(None, lambda: self.update_loop, "UpdateLoop").start()

    def onItemSelected(self, evt):
        # if self.currentItem is not None:
        #     self.test_list.Select(self.currentItem, 0)
        self.currentItem = evt.GetIndex()

    def onItemDeselected(self, evt):
        self.test_list.Select(evt.GetIndex(), 1)
        print("Deselect")

    def update_loop(self):
        global total_value
        global total_progress
        isActive = app.IsActive()
        while isActive:
            # frame.Update()
            # # panel.Update()
            # self.Update()
            # # self.update()
            # self.progress.SetRange(total_value)
            # self.progress.SetValue(total_progress)
            # self.progress.Update()
            frame.Update()
            frame.Refresh(False)
            frame.UpdateWindowUI(wx.UPDATE_UI_PROCESS_ALL)

            frame.OnInternalIdle()

            self.progress.SetRange(total_value)
            self.progress.SetValue(total_progress)

            time.sleep(0.1)
            isActive = app.IsActive()

    def test(self, evt):
        global total_progress
        global total_value
        if self.currentItem == 0:
            self.seedint_test()
        if self.currentItem == 1:
            self.overwrite_offset()

    def write(self, o):
        self.log.AppendText(str(o))
        # sys.__stdout__.write(o)

    def flush(self):
        # self.log.Update()
        # sys.__stdout__.flush()
        pass

    def overwrite_offset(self):
        import os

        # import urllib.request
        # a = urllib.request.urlopen("http://releases.ubuntu.com/19.10/SHA256SUMS.gpg")
        # print(a.__dict__)
        # # a.seek((128*1024*1024)*1)
        # # Note: This code will not work on online IDE

        # Importing the required packages
        import click
        import requests
        import threading

        # The below code is used for each chunk of file handled
        # by each thread for downloading the content from specified
        # location to storage
        def Handler(start, end, url, filename):

            # specify the starting and ending of the file
            headers = {'Range': 'bytes=%d-%d' % (start, end)}

            # request the specified part and get into variable
            r = requests.get(url, headers=headers, stream=True)

            # open the file and write the content of the html page
            # into file.
            with open(filename, "r+b") as fp:

                fp.seek(start)
                var = fp.tell()
                fp.write(r.content)

        @click.command(help="It downloads the specified file with specified name")
        @click.option('—number_of_threads', default=4, help="No of Threads")
        @click.option('--name', type=click.Path(), help="Name of the file with extension")
        @click.argument('url_of_file', type=click.Path())
        @click.pass_context
        def download_file(ctx, url_of_file, name, number_of_threads):
            r = requests.head(url_of_file)
            if name:
                file_name = name
            else:
                file_name = url_of_file.split('/')[-1]
            try:
                file_size = int(r.headers['content-length'])
            except:
                print("Invalid URL")
                return

            part = int(file_size) / number_of_threads
            fp = open(file_name, "wb")
            fp.write(b'\0' * file_size)
            fp.close()

            for i in range(number_of_threads):
                start = part * i
                end = start + part

                # create a Thread with start and end locations
                t = threading.Thread(target=Handler,
                                     kwargs={'start': start, 'end': end, 'url': url_of_file, 'filename': file_name})
                t.setDaemon(True)
                t.start()

            main_thread = threading.current_thread()
            for t in threading.enumerate():
                if t is main_thread:
                    continue
                t.join()
            print('%s downloaded' % file_name)

        if __name__ == '__main__':
            download_file(obj={})

        download_file(None, "http://releases.ubuntu.com/19.10/SHA256SUMS.gpg", "TestFile.gpg", 4)

        # if os.path.exists("offset_file.qdata"):
        #     os.remove("offset_file.qdata")
        # data1 = b"".join(bytes(16))
        # print("Data Length: %s bytes" % 16)
        # print("Data Content: %s" % data1)
        # with open("offset_file.qdata", "wb+") as file:
        #     file.write(data1)
        # with open("offset_file.qdata", "rb+") as file:
        #     file.seek(3)
        #     file.tell()
        #     file.write(bytearray(3))
        #     print("Data at offset 0x00000003 is set to %s" % bytearray(3))
        # with open("offset_file.qdata", "rb") as file:
        #     data2 = file.read(16)
        #
        # print("Data Length: %s bytes" % 16)
        # print("Data Content: %s" % data2)

    def seedint_test(self):
        global total_progress
        global total_value

        def seedint_lookup(i, minimal, maximal):
            return int((((i + 1) / 2) * (maximal - minimal)) + minimal)

        def seedint(seed, x, y, minimal, maximal, **debug_opt):
            from opensimplex import OpenSimplex
            import sys

            # print("Minimal: %s" % minimal)
            # print("Minimal: %s" % maximal)

            out = OpenSimplex(seed).noise2d(x, y)
            out = ((out + 1+(11/9/7/3)) / 2)
            if debug_opt["_test_seed"] is True:
                if round(out, 1) == 1.0 or round(out, 1) == -1.0:
                    sys.stdout.write("||x:%s|y:%s|out:%s||\n" % (x, y, out))
                else:
                    if debug_opt["verbose"] is True:
                        sys.stderr.write("||x:%s|y:%s|out:%s||" % (x, y, out))

            out2 = (out * (maximal - minimal)) + minimal
            if out2 == maximal:
                # print("\n\nOutput is the same as maximal")
                if debug_opt["verbose"] is True:
                    print("Output hits the maximum")
                out2is_maximal = True
            else:
                out2is_maximal = False
            return out2, out2is_maximal
            # return int((((out + 1) / 2) * (maximal - minimal)) + minimal)

        def seed(seed, x, y):
            from opensimplex import OpenSimplex

            out = OpenSimplex(seed).noise2d(x, y)
            # return int((((out + 1) / 2) * (maximal - minimal)) + minimal)

        def num_dialog(*args, **kwargs):
            a = wx.NumberEntryDialog(*args, **kwargs)
            a.ShowWindowModal()
            return a.GetValue()

        def txt_dialog(*args, **kwargs):
            a = wx.TextEntryDialog(*args, **kwargs)
            a.ShowWindowModal()
            return a.GetValue()

        import math
        _x_min = num_dialog(frame, "Enter a Minimal X Value", "prompt", "caption", 0, -2000, 2000)
        _x_max = num_dialog(frame, "Enter a Maximal X Value", "prompt", "caption", 0 if _x_min <= 0 else _x_min, -2000,
                            2000)

        _y_min = num_dialog(frame, "Enter a Minimal Y Value", "prompt", "caption", 0, -2000, 2000)
        _y_max = num_dialog(frame, "Enter a Maximal Y Value", "prompt", "caption", 0 if _y_min <= 0 else _y_min, -2000,
                            2000)

        # _x_range_str = input("X Range (<min>-<max>):")
        # _y_range_str = input("Y Range (<min>-<max>):")

        _x_range = range(_x_min, _x_max)
        _y_range = range(_y_min, _y_max)

        _min = num_dialog(frame, "Enter a Minimal Value", "prompt", "caption", 0, -2000, 2000)
        _max = num_dialog(frame, "Enter a Maximal Value", "prompt", "caption", 0 if _min <= 0 else _min, _min, 2000)
        _seed = num_dialog(frame, "Enter a Seed", "prompt", "caption", 65535, -1000000000, 1000000000)

        # _min = int(input("Minimal Value: "))
        # _max = int(input("Maximal Value: "))
        # _seed = int(input("Seed: "))
        _highest_out = -math.inf
        _is_max = False

        _temp29c4 = len(_x_range)
        _temp593b = len(_y_range)
        total_length = _temp29c4 * _temp593b
        total_value = total_length

        def seedint_test2(_highest_out, _x_range, _y_range, _is_max):
            global total_progress
            global total_value
            for x in _x_range:
                for y in _y_range:
                    output, is_max = seedint(_seed, x, y, _min, _max, _test_seed=True, verbose=False)
                    if _highest_out < output:
                        _highest_out = output
                    if is_max is True:
                        _is_max = True

                    # frame.Update()
                    # frame.Refresh(True)
                    # frame.UpdateWindowUI(wx.UPDATE_UI_PROCESS_ALL)
                    # frame.OnInternalIdle()
                    # self.test_btn.Update()
                    # self.test_btn.Refresh(True)

                    self.progress.SetRange(total_value)
                    self.progress.SetValue(total_progress)

                    total_progress += 1
                    # self.Update()
                    # if wx.UpdateUIEvent.CanUpdate(self):
                    #     self.UpdateWindowUI(wx.UPDATE_UI_FROMIDLE)
                    # self.OnInternalIdle()
                    # self.progress.Update()
                    # self.progress.OnInternalIdle()

            if _is_max is True:
                print("[OUT]: Output was hit the maximum value")
            else:
                print("[OUT]: Output was not hit the maximum value")

            print("[OUT]: Highest output was %s" % _highest_out)

        Thread(None, lambda: seedint_test2(_highest_out, _x_range, _y_range, _is_max)).start()

    # ----------------------------------------------------------------------
    def add_line(self, text):
        # line = "Line %s" % self.index
        line = text
        self.test_list.InsertItem(self.index, line)
        # self.test_list.SetItem(self.index, 1, "01/19/2010")
        # self.test_list.SetItem(self.index, 2, "USA")
        self.index += 1


import wx


########################################################################
class MyForm(wx.Frame):

    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "List Control Tutorial")

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.index = 0

        self.list_ctrl = wx.ListCtrl(panel, size=(-1, 100),
                                     style=wx.LC_REPORT
                                           | wx.BORDER_SUNKEN
                                     )
        self.list_ctrl.InsertColumn(0, 'Subject')
        self.list_ctrl.InsertColumn(1, 'Due')
        self.list_ctrl.InsertColumn(2, 'Location', width=125)

        btn = wx.Button(panel, label="Add Line")
        btn.Bind(wx.EVT_BUTTON, self.add_line)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(sizer)

    # ----------------------------------------------------------------------
    def add_line(self, event):
        line = "Line %s" % self.index
        self.list_ctrl.InsertItem(self.index, line)
        self.list_ctrl.SetItem(self.index, 1, "01/19/2010")
        self.list_ctrl.SetItem(self.index, 2, "USA")
        self.index += 1
#
#
# # ----------------------------------------------------------------------
# # Run the program
# if __name__ == "__main__":
#     app = wx.App(False)
#     frame = MyForm()
#     frame.Show()
#     app.MainLoop()


if __name__ == "__main__":
    # tests = """Choose a test:
    # (0) Seedint Test
    # """
    app = wx.App(False)
    # tests = {"Seedint Test": lambda: seedint_test()}
    # # print(tests)
    # # i = input("INPUT:")
    # if int(i) == 0:
    #     seedint_test()
    frame = wx.Frame(None, wx.ID_ANY, "Test Panel")
    frame.SetMinSize((700, 700))
    frame.SetMaxSize((700, 700))
    panel = TestPanel(frame)
    frame.Show()
    app.MainLoop()
