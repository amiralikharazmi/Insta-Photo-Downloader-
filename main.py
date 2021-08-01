from time import sleep
from threading import Timer
from datetime import datetime, timedelta
from ttkbootstrap import Style
from instaloader import Instaloader, Profile
from instaloader.exceptions import BadCredentialsException, InvalidArgumentException, ConnectionException, \
    TwoFactorAuthRequiredException, ProfileNotExistsException
from tkinter import *
from PIL import ImageTk as IK
from PIL import Image, ImageDraw
from tkinter.messagebox import showerror, askyesno
import os
from numpy import dstack, array


def get_fileNames(dir):
    fs = list()
    for path, dirname, files in os.walk(dir, topdown=True):
        for name in files:
            _, ending = os.path.splitext(name)
            if ending == ".jpg" or ending == '.png':
                fs.append(os.path.join(path, name))
    return fs


class Insta_Downloader:
    def __init__(self, _root):
        # define variables
        self.dlbl = self.lbl_info_img = self.status = self.lbl_image = self.lbl_user = self.img_lbl = Label()
        self.user_label = self.pass_label = self.user_code = Label()
        self.text_pass = self.text_user = self.dtext_user = self.text_code = Entry()
        self.login_frame = self.downloader_frame = Frame()
        self.login_btn = self.button_next = self.button_pre = Button()
        self.image_posts = int()
        self.List_images = list()
        self.root = _root

        self.root.configure(bg='gray19')
        self.root.title('Insta Photo Downloader')
        self.root.geometry("1280x700+100+50")
        self.root.resizable(False, False)
        self.menu()
        # set login frame
        self.login_frame = Frame(self.root, bg='snow')
        self.login_frame.place(x=385, y=50, height=600, width=500)
        self.title = Label(self.login_frame, text='Welcome Back!', bg='snow', fg='gray15',
                           font=('Impact', '35', 'bold'))
        self.title.place(x=80, y=20)
        self.description = Label(self.login_frame, text='Login to your instagram account', bg='snow', fg='gray15',
                                 font=('Book Antiqua', '15', 'bold'))
        self.description.place(x=80, y=90)
        self.user_label = Label(self.login_frame, text='Username', bg='snow', fg='gray15',
                                font=('times new roman', '15'))
        self.user_label.place(x=80, y=160)
        self.text_user = Entry(self.login_frame, bg='white', font=('times new roman', '15'), fg='black')
        self.text_user.place(x=80, y=190, width=350, height=35)
        self.pass_label = Label(self.login_frame, text='Password', bg='snow', fg='gray15',
                                font=('times new roman', '15'))
        self.pass_label.place(x=80, y=230)
        self.text_pass = Entry(self.login_frame, bg='white', font=('times new roman', '15'), fg='black', show='*')
        self.text_pass.place(x=80, y=260, width=350, height=35)
        self.login_btn = Button(self.login_frame, text='Login', command=self.login, bg='black', fg='white', bd=4,
                                font=('times new roman', '20'))
        self.login_btn.place(x=170, y=380, width=150, height=50)

    def download_post(self):
        self.downloader_frame.place_forget()
        self.login_frame.place_forget()
        username = self.dtext_user.get()
        posts = Profile.from_username(mode.context, username=username).get_posts()
        self.image_posts = 0
        for p in posts:
            if not p.is_video:
                self.image_posts += 1
        if self.image_posts == 0:
            self.dlbl = Label(self.root, bg='gray19', fg='white', font=('times new roman', '40', 'bold'),
                              text=f"This user's sage is private or has no any photo!")
            self.dlbl.place(relx=0.5, rely=0.5, anchor=CENTER)
            return
        self.dlbl = Label(self.root, bg='gray19', fg='white', font=('times new roman', '50', 'bold'),
                          text=f'downloading {self.image_posts} photos')
        self.dlbl.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.root.after(1, self.download_status())
        posts = Profile.from_username(mode.context, username=username).get_posts()
        for post in posts:
            if not post.is_video:
                mode.download_post(post=post, target=f'{username}')

        self.show_photos()

    def download_status(self):
        current_status = self.dlbl['text']

        if current_status.endswith("..."):
            current_status = f'downloading {self.image_posts} photos'

        else:
            current_status += "."

        self.dlbl['text'] = current_status

        root.after(1000, self.download_status)

    def login_status(self):
        current_status = self.status['text']

        if current_status.endswith("..."):
            current_status = f'Logging'

        else:
            current_status += "."

        self.status['text'] = current_status

        root.after(1000, self.login_status)

    def verify_status(self):
        current_status = self.status['text']

        if current_status.endswith("..."):
            current_status = f'Logging'

        else:
            current_status += "."

        self.status['text'] = current_status

        root.after(1000, self.verify_status)

    def show_photos(self):
        self.dlbl.place_forget()
        username = self.dtext_user.get()
        photos = get_fileNames(username)

        for photo in photos:
            self.List_images.append(IK.PhotoImage(Image.open(photo).resize((580, 650))))
        self.List_images.reverse()
        self.img_lbl = Label(image=self.List_images[0])

        self.img_lbl.place(relx=0.5, rely=0, anchor=N)
        self.lbl_info_img = Label(self.root, bg='gray19', fg='gray30', text=f'1/{len(self.List_images)}',
                                  font=('the new roman', '15'))
        self.lbl_info_img.place(relx=0.5, rely=1, anchor=S)
        self.button_pre = Button(self.root, text="<", command=self.previous,
                                 state=DISABLED, font=('the new roman', '20'), bg='gray19', fg='gray15')

        self.button_next = Button(self.root, text=">", command=lambda: self._next(1), font=('the new roman', '20'),
                                  bg='gray19', fg='gray30')

        self.button_pre.place(rely=0.5, anchor=W, height=700, width=70)
        self.button_next.place(relx=1.0, rely=0.5, anchor=E, height=700, width=70)

    def _next(self, img_no):
        self.img_lbl.place_forget()
        self.button_next.place_forget()
        flag = True
        self.img_lbl = Label(image=self.List_images[img_no])
        self.img_lbl.place(relx=0.5, rely=0, anchor=N)
        self.lbl_info_img.config(text=f'{img_no + 1}/{len(self.List_images)}')
        if img_no == len(self.List_images) - 1:
            flag = False
            self.button_next = Button(self.root, text=">", state=DISABLED, font=('the new roman', '20'), bg='gray19',
                                      fg='gray15')
        self.button_pre = Button(self.root, text="<",
                                 command=lambda: self.previous(img_no - 1), font=('the new roman', '20'), bg='gray19',
                                 fg='gray30')
        if flag:
            self.button_next = Button(self.root, text=">",
                                      command=lambda: self._next(img_no + 1), font=('the new roman', '20'), bg='gray19',
                                      fg='gray30')

        self.button_pre.place(rely=0.5, anchor=W, height=700, width=70)
        self.button_next.place(relx=1.0, rely=0.5, anchor=E, height=700, width=70)

    def previous(self, img_no):

        self.img_lbl.place_forget()
        self.button_pre.place_forget()
        flag = True
        self.img_lbl = Label(image=self.List_images[img_no])
        self.img_lbl.place(relx=0.5, rely=0, anchor=N)
        self.lbl_info_img.config(text=f'{img_no + 1}/{len(self.List_images)}')
        if img_no == 0:
            flag = False
            self.button_pre = Button(self.root, text="<", state=DISABLED, font=('the new roman', '20'), bg='gray19',
                                     fg='gray30')
        self.button_next = Button(self.root, text=">",
                                  command=lambda: self._next(img_no + 1), font=('the new roman', '20'), bg='gray19',
                                  fg='gray30')
        if flag:
            self.button_pre = Button(self.root, text="<",
                                     command=lambda: self.previous(img_no - 1), font=('the new roman', '20'),
                                     bg='gray19', fg='gray30')

        self.button_pre.place(rely=0.5, anchor=W, height=700, width=70)
        self.button_next.place(relx=1.0, rely=0.5, anchor=E, height=700, width=70)

    def convertor(self, photo):

        png_photo = photo.replace(photo.split('.')[-1], 'png')

        image = Image.open(photo)
        image.save(png_photo)
        # Open the input image as numpy array, convert to RGB
        img = Image.open(png_photo).convert('RGB')
        npImage = array(img)
        h, w = img.size
        username = self.dtext_user.get()
        # Create same size alpha layer with circle
        alpha = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(alpha)
        draw.pieslice([0, 0, h, w], 0, 360, fill=255)

        # Convert alpha Image to numpy array
        npAlpha = array(alpha)

        # Add alpha layer to RGB
        npImage = dstack((npImage, npAlpha))

        # Save with alpha

        Image.fromarray(npImage).save(f'edit-{username}.png')
        return True

    def two_step(self):
        self.forget()
        self.title.config(text='Two-step verification')
        self.title.place(x=30, y=20)
        self.description.config(text='Code was sent to your email or phone number.')
        self.description.place(x=30, y=90)
        self.user_code = Label(self.login_frame, text='Code', bg='snow', fg='gray15',
                               font=('times new roman', '15'))
        self.user_code.place(x=70, y=160)
        self.text_code = Entry(self.login_frame, fg='black', bg='white', font=('times new roman', '15'))
        self.text_code.place(x=70, y=190, width=350, height=35)
        self.login_btn.config(text='Verify', command=self.two_step_login)
        self.login_btn.place(x=180, y=310, width=150, height=50)
        resend_req = Button(self.login_frame, text='Resend Code',
                            command=self.login,
                            bg='snow', fg='gray15',
                            font=('times new roman', '10'), bd=1)
        resend_req.place(x=70, y=225, width=70, height=30)

    def two_step_login(self):
        if self.text_code.get() == "":
            showerror(title='Error', message='Code can not be empty!')
            return
        elif len(self.text_code.get()) != 6:
            showerror('Error', 'Code must be 6 digits long!')
            self.text_code.delete(first=0, last=END)
            return
        elif not self.text_code.get().isdigit():
            showerror('Error', 'Code must be contain numbers only!')
            self.text_code.delete(first=0, last=END)
            return
        else:
            code = int(self.text_code.get())
            self.status.place_forget()
            self.status.config(text='verifying')
            self.status.place(relx=0, rely=1, anchor=SW)
            self.root.after(1, self.verify_status())
            try:

                sleep(1)
                mode.two_factor_login(code)

            except InvalidArgumentException:
                showerror('Error', 'No two-factor authentication pending.')
            except BadCredentialsException:
                showerror('Error', '2FA verification code invalid.')
            self.status.place_forget()
        if mode.test_login() is not None:
            self.show()

    def set_following_list(self):
        following_list = list()
        username = self.text_user.get()
        profile = Profile.from_username(context=mode.context, username=username)
        followings = profile.get_followees()
        for flw in followings:
            following_list.append(flw.username)
        return following_list

    def show(self):
        self.downloader_frame = Frame(self.root, bg='white')
        self.downloader_frame.place(x=385, y=50, height=600, width=500)
        title = Label(self.downloader_frame, text='Downloader', bg='white', fg='gray15',
                      font=('Impact', '35', 'bold'))
        description = Label(self.downloader_frame,
                            text='Enter the username of your friend \nwhose photos you want to see.', bg='white',
                            fg='gray15',
                            font=('Book Antiqua', '15', 'bold'))
        description.place(x=80, y=90)
        title.place(x=120, y=20)
        image = Image.open('edit-user.png')
        resized_img = image.resize((200, 200))
        self.image = IK.PhotoImage(resized_img)
        self.lbl_image = Label(self.downloader_frame, image=self.image)
        self.lbl_image.place(x=145, y=170)
        self.lbl_user = Label(self.downloader_frame, text='Username', bg='white', fg='gray15',
                              font=('times new roman', '15'))
        self.lbl_user.place(x=80, y=390)
        self.dtext_user = Entry(self.downloader_frame, bg='white', font=('times new roman', '15'), fg='black')
        self.dtext_user.place(x=80, y=420, width=350, height=35)
        download_btn = Button(self.downloader_frame, text='Download', command=self.update, bg='black', fg='white',
                              bd=4, font=('times new roman', '20'))
        download_btn.place(x=180, y=490, width=150, height=50)

    def update(self):
        pic_path = str()
        username = self.dtext_user.get()
        try:
            p = Profile.from_username(mode.context, username)
            mode.download_profilepic(p)
        except ProfileNotExistsException:
            self.downloader_frame.place_forget()
            lbl = Label(self.root, bg='gray19', fg='white', font=('times new roman', '40', 'bold'),
                        text=f"This username does not exist!")
            lbl.place(relx=0.5, rely=0.5, anchor=CENTER)
        for name in get_fileNames(username):
            if 'profile_pic.jpg' in name:
                pic_path = name
        if self.convertor(pic_path):
            img = Image.open(f'edit-{username}.png')
            resized_img = img.resize((200, 200))
            self.image = IK.PhotoImage(resized_img)
            self.lbl_image.config(image=self.image)
            self.lbl_image.place(x=145, y=170)
            for file_path in get_fileNames(username):
                os.remove(file_path)
            os.rmdir(username)
            os.remove(f'edit-{username}.png')
            x = datetime.today()
            z = timedelta(days=x.day, hours=x.hour, minutes=x.minute, seconds=x.second + 2, microseconds=x.microsecond)
            y = timedelta(days=x.day, hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
            delta_t = z - y
            Timer(delta_t.seconds, self.download_post).start()

    def login(self):
        if self.text_user.get() == "" or self.text_pass.get() == "":
            showerror(title='Error', message='Username and password can not be empty!')
            return
        elif len(self.text_pass.get()) < 4:
            showerror('Error', 'Password must be longer than four character!')
            self.text_pass.delete(first=0, last=END)
            return
        else:
            username = self.text_user.get()
            password = self.text_pass.get()

            try:
                self.status = Label(self.login_frame, text='Logging', bg='snow', fg='gray19',
                                    font=('Book Antiqua', '15', 'bold'))
                self.status.place(relx=0, rely=1, anchor=SW)
                self.root.after(1, self.login_status())
                mode.login(user=username, passwd=password)


            except BadCredentialsException:
                showerror('Error', 'the provided password is wrong.')
                self.text_pass.delete(first=0, last=END)
            except InvalidArgumentException:
                showerror('Error', 'the provided username does not exist.')
                self.text_user.delete(first=0, last=END)
                self.text_pass.delete(first=0, last=END)
            except ConnectionException:
                showerror('Error', 'connection to Instagram failed.')
                self.text_user.delete(first=0, last=END)
                self.text_pass.delete(first=0, last=END)
            except TwoFactorAuthRequiredException:
                self.forget()
                self.two_step()
            self.status.place_forget()
        if mode.test_login() is not None:
            self.show()

    def forget(self):
        self.text_pass.place_forget()
        self.text_user.place_forget()
        self.login_btn.place_forget()
        self.user_label.place_forget()
        self.pass_label.place_forget()
        self.description.place_forget()
        self.status.place_forget()

    def about(self):
        self.login_frame.place_forget()
        label = Label(self.root, text="This app create for download and see your friend's instagram photos.",
                      bg='gray19', fg='white', font=('times new roman', '18')).place(relx=0.5, rely=0.1, anchor=N)
        return

    def help(self):
        self.login_frame.place_forget()
        label = Label(self.root,
                      text="To use this app, just log in to your instagram account and see your friend's photos by\n "
                           "entering your friend's username.",
                      bg='gray19', fg='white', font=('times new roman', '18')).place(relx=0.5, rely=0.1, anchor=N)
        return

    def Exit(self):
        msg = askyesno('exit', 'Do you wanna exit app?')
        if msg:
            self.root.destroy()

    def menu(self):
        menubar = Menu(self.root)
        menu = Menu(menubar, tearoff=0)
        menu.add_command(label="about", command=self.about)
        menu.add_command(label="Help", command=self.help)
        menubar.add_cascade(label="Menu", menu=menu)
        menu.add_command(label="Exit", command=self.Exit)
        menu.add_separator()

        self.root.config(menu=menubar)


style = Style()
root = style.master
mode = Instaloader()
ins = Insta_Downloader(root)
root.mainloop()
