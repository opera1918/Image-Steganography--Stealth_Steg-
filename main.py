import customtkinter
import os
import configparser
import pyperclip
from PIL import Image
from steno import txt_in_img
from steno import img_in_img

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.config = configparser.ConfigParser()
        self.config.read('app.conf')

        self.title("Data Confidentiality Using Steganography | (REC)")
        
        # Screen Configuration
        self.width = self.config.getint('Settings', 'window_width')
        self.height = self.config.getint('Settings', 'window_height')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_coordinate = int(self.screen_width//4) 
        self.y_coordinate = int(self.screen_height//6) 
        self.geometry(f"{self.width}x{self.height}+{self.x_coordinate}+{self.y_coordinate}")
        self.resizable(0, 0)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "stealth _steg_logo_dark.png")), dark_image=Image.open(os.path.join(image_path, "stealth_steg_logo_light.png")), size=(40, 40))
        self.img_in_txt_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "txt_in_img_dark.png")), dark_image=Image.open(os.path.join(image_path, "txt_in_img_light.png")), size=(20, 20))
        self.img_in_img_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "img_in_img_dark.png")), dark_image=Image.open(os.path.join(image_path, "img_in_img_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="news")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

 
        self.navigation_frame_label = customtkinter.CTkButton(self.navigation_frame, text=" Stealth_Steg", image=self.logo_image, compound="left", font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="transparent", hover_color=("gray17","gray17"), command=self.introduction_stegano_button_event)
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.image_txt = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Text In Image (LSB)", fg_color="transparent", bg_color="grey20", text_color=("gray10", "gray90"), hover_color="#1a1a1a", image=self.img_in_txt_icon, anchor="w", command=self.image_txt_stegano_button_event)
        self.image_txt.grid(row=1, column=0, sticky="ew")

        self.image_img = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Image In Image (LSB)", fg_color="transparent", bg_color="grey20", text_color=("gray10", "gray90"), hover_color="#1a1a1a", image=self.img_in_img_icon, anchor="w", command=self.image_img_stegano_button_event)
        self.image_img.grid(row=2, column=0, sticky="ew")

        # IN PROGRESS 
        self.audio_steno = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="          [In-Progress]  ",fg_color="transparent", bg_color="grey20", text_color=("gray10", "gray90"), hover_color="#1a1a1a", anchor="w", command=self.audio_steno_button_event)
        self.audio_steno.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # -=-=-=- INTRODUCTION -=-=-=-
        self.introduction = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.introduction.grid(row=0, column=1)

        self.introduction__about_frame = customtkinter.CTkFrame(self.introduction, corner_radius=10) #
        self.introduction__about_frame.grid(row=0, column=1, padx=10, pady=(18, 10))

        self.project_about_title = customtkinter.CTkLabel(self.introduction__about_frame, text="[ About ]", font=customtkinter.CTkFont(size=15, weight="bold"), width=700, text_color="#32d6f0")
        self.project_about_title.grid(row=0, column=1, padx=10, pady=10)

        self.project_about_content = customtkinter.CTkLabel(self.introduction__about_frame, text="This steganography project, named \"Data Confidentiality Using Steganography,\" aims to develop a pure Python application that can hide an image inside another image and text inside an image using the least significant bit (LSB) technique. \n\nThe project will incorporate advanced encryption standard (AES) encryption to enhance the security of the hidden data. To develop an intuitive and user-friendly interface, the application will utilize Custom Tkinter, along with various image processing and cryptography libraries in Python, to implement the hiding and encryption techniques. The goal of the project is to create an easy-to-use application that facilitates secure communication and data hiding.", font=customtkinter.CTkFont(size=15, weight="bold"), wraplength=670)
        self.project_about_content.grid(row=1, column=1, padx=10, pady=(0, 20), sticky="ew")


        self.introduction__future_scope_frame = customtkinter.CTkFrame(self.introduction, corner_radius=10) #
        self.introduction__future_scope_frame.grid(row=1, column=1, padx=10, pady=(0, 18)) 

        self.introduction__future_scope_title = customtkinter.CTkLabel(self.introduction__future_scope_frame, text="[ Future Scope ]", font=customtkinter.CTkFont(size=15, weight="bold"), width=705, text_color="#32d6f0")
        self.introduction__future_scope_title.grid(row=0, column=1, padx=(10, 5), pady=10)


        self.project_future_scope_content_1 = customtkinter.CTkLabel(self.introduction__future_scope_frame, text="[1] Integrating a Gmail service using Simple Mail Transfer Protocol (SMTP) would enable users to instantly share the Secret image and Security key via email, \njust in One-Click enhancing the usability of this application.", font=customtkinter.CTkFont(size=15, weight="bold"), wraplength=662)
        self.project_future_scope_content_1.grid(row=1, column=1, padx=25, pady=(0, 5), sticky="w")

        self.project_future_scope_content_2 = customtkinter.CTkLabel(self.introduction__future_scope_frame, text="[2] Incorporating batch processing functionality would allow users to hide multiple images or files at once, increasing the efficiency of the application.", font=customtkinter.CTkFont(size=15, weight="bold"), wraplength=662)
        self.project_future_scope_content_2.grid(row=2, column=1, padx=25, pady=5, sticky="w")

        self.project_future_scope_content_3 = customtkinter.CTkLabel(self.introduction__future_scope_frame, text="[3] Support other file formats, such as audio or video files, would increase its versatility and usefulness for data hiding and secure communication.", font=customtkinter.CTkFont(size=15, weight="bold"), wraplength=662)
        self.project_future_scope_content_3.grid(row=3, column=1, padx=25, pady=(5, 125), sticky="w")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # TEXT IN IMAGE

        self.image_txt_home = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.image_txt_home.grid(row=0, column=1)
 
        self.image_txt_tab = customtkinter.CTkTabview(self.image_txt_home, corner_radius=10)
        self.image_txt_tab.grid(row=0, column=0, sticky="ew", padx=10)

        # Encrypt Message in Image  
        self.image_txt_tab.add("Encrypt")
        self.image_txt_tab_container_e = customtkinter.CTkFrame(self.image_txt_tab.tab("Encrypt"), fg_color="transparent")
        self.image_txt_tab_container_e.grid(row=0, column=0, sticky="ew", padx=10)

        self.image_txt_msg_title_e = customtkinter.CTkLabel(self.image_txt_tab_container_e, text="Message",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.image_txt_msg_title_e.grid(row=0, column=0, padx=10, pady=5, sticky="w") # Message Title

        self.image_txt_msg_e = customtkinter.CTkTextbox(self.image_txt_tab_container_e,  width=655, height= 150,corner_radius=10)
        self.image_txt_msg_e.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="news") # Message Textbox

        self.image_txt_fetch_txtfile_btn_e = customtkinter.CTkButton(self.image_txt_tab_container_e, text="Fetch textual file", command=self.open_txtfile)
        self.image_txt_fetch_txtfile_btn_e.grid(row=2, column=0, padx=(10, 10), pady=5, sticky="ew") # Fetch txt file button

        self.image_txt_fetch_txtfile_path_e = customtkinter.CTkTextbox(self.image_txt_tab_container_e, width=450, height=10)
        self.image_txt_fetch_txtfile_path_e.grid(row=2, column=1, columnspan=2, padx=(5,10), pady=5, sticky="ew") # Fetch txt path textbox

        self.image_txt_select_img_title_e = customtkinter.CTkLabel(self.image_txt_tab_container_e, text="Select Image",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.image_txt_select_img_title_e.grid(row=3, column=0, padx=10, pady=(34, 5), sticky="w") # Select Image Button

        self.image_txt_output_title_e = customtkinter.CTkLabel(self.image_txt_tab_container_e, text="Output Image Path",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.image_txt_output_title_e.grid(row=3, column=1, padx=10, pady=(34, 10), sticky="w") # Select Image Button

        self.image_txt_static_imgfile_e = customtkinter.CTkImage(Image.open(os.path.join(image_path, "initial_img.jpg")), size=(165, 165))
        self.image_txt_static_imgfile_prev_e = customtkinter.CTkLabel(self.image_txt_tab_container_e, text="", image=self.image_txt_static_imgfile_e, corner_radius=10, fg_color="gray100", height=180, width=170)
        self.image_txt_static_imgfile_prev_e.grid(row=4, column=0, columnspan=1, padx=10, pady=5, sticky="ew") # Static initial image

        self.image_txt_output_path_e = customtkinter.CTkLabel(self.image_txt_tab_container_e, text="",  font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="gray90", height=180, width=450, corner_radius=10, wraplength=450)
        self.image_txt_output_path_e.grid(row=4, column=1, padx=10, pady=(5, 5), sticky="ew")

        self.image_txt_fetch_imgfile_btn_e = customtkinter.CTkButton(self.image_txt_tab_container_e, text="Select Image file", command=self.open_imgfile_e)
        self.image_txt_fetch_imgfile_btn_e.grid(row=5, column=0, padx=(10, 10), pady=(5, 0), sticky="ew")

        self.image_txt_embed_btn_e = customtkinter.CTkButton(self.image_txt_tab_container_e, text="Embed Message", command=self.image_txt_embed_msg_e)
        self.image_txt_embed_btn_e.grid(row=5, column=1, padx=(10, 10), pady=(10, 0), sticky="ew") 

        # Decrypt Message in Image
        self.image_txt_tab.add("Decrypt")
        self.image_txt_tab_container_d = customtkinter.CTkFrame(self.image_txt_tab.tab("Decrypt"), corner_radius=0, fg_color="transparent")
        self.image_txt_tab_container_d.grid(row=0, column=1, sticky='ew')
        self.image_txt_tab_container_d.columnconfigure((0, 1), weight=1)
        self.image_txt_tab_container_d.rowconfigure((0, 2, 3, 4), weight=1)
        # self.image_txt_tab_container_d.rowconfigure((1), weight=2)


        self.image_txt_secimg_title_d =  customtkinter.CTkLabel(self.image_txt_tab_container_d, text="Secret Image", corner_radius=10, fg_color="transparent",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.image_txt_secimg_title_d.grid(row=0, column=0, padx=9, pady=5, sticky="w") #

        self.image_txt_secimg_title_d =  customtkinter.CTkLabel(self.image_txt_tab_container_d, text="Hidden Message", corner_radius=10, fg_color="transparent",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.image_txt_secimg_title_d.grid(row=0, column=1, padx=14, pady=5, sticky="w") #

        self.image_txt_static_imgfile_d = customtkinter.CTkImage(Image.open(os.path.join(image_path, "initial_img.jpg")), size=(250, 250))
        self.image_txt_static_imgfile_prev_d = customtkinter.CTkLabel(self.image_txt_tab_container_d, text="", image=self.image_txt_static_imgfile_d, corner_radius=10, fg_color="gray90", width=250, height=250)
        self.image_txt_static_imgfile_prev_d.grid(row=1, column=0, padx=(20,20), pady=(5, 0), sticky="news") # Static initial image
        
        self.image_txt_fetch_imgfile_btn_d = customtkinter.CTkButton(self.image_txt_tab_container_d, text="Select Image file", command=self.open_imgfile_d)
        self.image_txt_fetch_imgfile_btn_d.grid(row=2, column=0, padx=(17, 17), pady=(15, 10), sticky="new")

        self.image_txt_hidden_msg_d = customtkinter.CTkTextbox(self.image_txt_tab_container_d, width=339, height=492, corner_radius=10)
        self.image_txt_hidden_msg_d.grid(row=1, rowspan=4, column=1 ,padx=(25, 20), pady=(5,0), sticky="new") # Fetch txt path textbox

        self.image_txt_extract_btn_d = customtkinter.CTkButton(self.image_txt_tab_container_d, text="Enter Your Secret Key", command=self.image_txt_secret_key_dialogue_d, height=40, width=10)
        self.image_txt_extract_btn_d.grid(row=3, column=0, padx=(17, 17), pady=(90,0), sticky="sew")

        self.image_txt_extract_btn_d = customtkinter.CTkButton(self.image_txt_tab_container_d, text="Extract Hidden Message", command=self.extract_hidden_msg_d, height=40, width=10)
        self.image_txt_extract_btn_d.grid(row=4, column=0, padx=(17, 17), pady=(10, 0), sticky="ews")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # IMAGE IN IMAGE 

        self.image_img_home = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.image_img_home.grid(row=0, column=1)

        self.image_img_tab = customtkinter.CTkTabview(self.image_img_home, corner_radius=10)
        self.image_img_tab.grid(row=0, column=0, sticky="ew", padx=10)

        # Encrypt Image in Image  
        self.image_img_tab.add("Encrypt")
        self.image_img_tab_container_e = customtkinter.CTkFrame(self.image_img_tab.tab("Encrypt"), fg_color="transparent")
        self.image_img_tab_container_e.rowconfigure((1), weight=1)
        self.image_img_tab_container_e.columnconfigure((0, 1), weight=1)
        self.image_img_tab_container_e.grid(row=0, column=0, sticky="ew", padx=10)

        self.image_img_cover_title_e = customtkinter.CTkLabel(self.image_img_tab_container_e, text="Cover Image", corner_radius=10, fg_color="transparent",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.image_img_cover_title_e.grid(row=0, column=0, padx=(0, 45), pady=5, sticky="w") #

        self.image_img_secret_title_e = customtkinter.CTkLabel(self.image_img_tab_container_e, text="Secret Image", corner_radius=10, fg_color="transparent",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.image_img_secret_title_e.grid(row=0, column=1, padx=(45, 0), pady=5, sticky="w") #


        self.image_img_static_imgfile_e = customtkinter.CTkImage(Image.open(os.path.join(image_path, "initial_img.jpg")), size=(250, 250))
        
        self.image_img_cover_imgfile_prev_e = customtkinter.CTkLabel(self.image_img_tab_container_e, text="", image=self.image_img_static_imgfile_e, corner_radius=10, fg_color="gray90", width=250, height=250)
        self.image_img_cover_imgfile_prev_e.grid(row=2, column=0, padx=(10, 57), pady=(5, 0), sticky="news")

        self.image_img_secret_imgfile_prev_e = customtkinter.CTkLabel(self.image_img_tab_container_e, text="", image=self.image_img_static_imgfile_e, corner_radius=10, fg_color="gray90", width=250, height=250)
        self.image_img_secret_imgfile_prev_e.grid(row=2, column=1, padx=(57, 10), pady=(5, 0), sticky="news")

        self.image_img_cover_imgfile_btn_e = customtkinter.CTkButton(self.image_img_tab_container_e, text="Select Cover Image", command=self.open_cover_imgfile_e)
        self.image_img_cover_imgfile_btn_e.grid(row=3, column=0, padx=(10, 53), pady=10, sticky="new")

        self.image_img_secret_imgfile_btn_e = customtkinter.CTkButton(self.image_img_tab_container_e, text="Select Secret Image", command=self.open_secret_imgfile_e)
        self.image_img_secret_imgfile_btn_e.grid(row=3, column=1, padx=(53, 10), pady=10, sticky="new")

        self.image_img_output_title_e =  customtkinter.CTkLabel(self.image_img_tab_container_e, text="Output Image Path", corner_radius=10, fg_color="transparent",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.image_img_output_title_e.grid(row=4, column=0, padx=0, pady=5, sticky="w")

        self.image_img_output_log_e = customtkinter.CTkLabel(self.image_img_tab_container_e, text="",  font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="gray90", width=650, height=120, corner_radius=10)
        self.image_img_output_log_e.grid(row=5, column=0, columnspan=2)

        self.image_img_embed_btn_e = customtkinter.CTkButton(self.image_img_tab_container_e, text="Embed Image", command=self.image_img_embed_img_e)
        self.image_img_embed_btn_e.grid(row=6, column=0, columnspan=2, padx=(10, 10), pady=(10, 2), sticky="ew") 

        # Decrypt Image in Image  
        self.image_img_tab.add("Decrypt")
        self.image_img_tab_container_d = customtkinter.CTkFrame(self.image_img_tab.tab("Decrypt"), fg_color="transparent")
        self.image_img_tab_container_d.rowconfigure((1), weight=1)
        self.image_img_tab_container_d.columnconfigure((0, 1), weight=1)
        self.image_img_tab_container_d.grid(row=0, column=0, sticky="ew", padx=10)

        self.image_img_secret_title_d = customtkinter.CTkLabel(self.image_img_tab_container_d, text="Secret Image", corner_radius=10, fg_color="transparent",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.image_img_secret_title_d.grid(row=0, column=0, padx=(0, 45), pady=5, sticky="w") #

        self.image_img_hidden_title_d = customtkinter.CTkLabel(self.image_img_tab_container_d, text="Hidden Image", corner_radius=10, fg_color="transparent",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.image_img_hidden_title_d.grid(row=0, column=1, padx=(45, 0), pady=5, sticky="w") #

        self.image_img_static_imgfile_d = customtkinter.CTkImage(Image.open(os.path.join(image_path, "initial_img.jpg")), size=(250, 250))

        self.image_img_secret_imgfile_prev_d = customtkinter.CTkLabel(self.image_img_tab_container_d, text="", image=self.image_img_static_imgfile_d, corner_radius=10, fg_color="gray90", width=250, height=250)
        self.image_img_secret_imgfile_prev_d.grid(row=2, column=0, padx=(10, 57), pady=(5, 0), sticky="news") 
        
        self.image_img_hidden_imgfile_prev_d = customtkinter.CTkLabel(self.image_img_tab_container_d, text="", image=self.image_img_static_imgfile_d, corner_radius=10, fg_color="gray90", width=250, height=250)
        self.image_img_hidden_imgfile_prev_d.grid(row=2, column=1, padx=(57, 10), pady=(5, 0), sticky="news") 

        self.image_img_secret_imgfile_btn_d = customtkinter.CTkButton(self.image_img_tab_container_d, text="Select Secret Image", command=self.open_secret_imgfile_d)
        self.image_img_secret_imgfile_btn_d.grid(row=3, column=0, padx=(10, 53), pady=10, sticky="new")
    
        self.image_img_secret_key_title_d = customtkinter.CTkLabel(self.image_img_tab_container_d, text="Secret Key", corner_radius=10, fg_color="transparent",  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.image_img_secret_key_title_d.grid(row=4, column=0, padx=(0, 0), pady=5, sticky="w") #

        self.image_img_secret_key_entry_d = customtkinter.CTkEntry(self.image_img_tab_container_d, placeholder_text="Your Secret Key", corner_radius=10, width=655, fg_color="transparent",  font=customtkinter.CTkFont(size=15, weight="bold"), bg_color="transparent")
        self.image_img_secret_key_entry_d.grid(row=5, column=0, columnspan=2 ,padx=(10, 10), pady=(5, 10), sticky="w") #

        self.image_img_output_path_d = customtkinter.CTkLabel(self.image_img_tab_container_d, text="",  font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="gray90", width=652, height=77, corner_radius=10)
        self.image_img_output_path_d.grid(row=6, column=0, columnspan=2, padx=0, pady=(0))

        self.image_img_extract_btn_d = customtkinter.CTkButton(self.image_img_tab_container_d, text="Extract Hidden Image", command=self.extract_hidden_img_d)
        self.image_img_extract_btn_d.grid(row=7, column=0, columnspan=2, padx=(10, 10), pady=(10, 2), sticky="ew") 


    
        # Audio Frame
        self.audio_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("intro")

    def select_frame_by_name(self, name):
        # set button color for selected button
        # self.introduction.configure(fg_color="transparent" if name == "intro" else "transparent")
        self.image_txt.configure(fg_color="red" if name == "image_txt" else "transparent")
        self.image_img.configure(fg_color="red" if name == "image_img" else "transparent")
        self.audio_steno.configure(fg_color="red" if name == "audio_txt" else "transparent")

        # show selected frame
        if name == "intro":
            self.introduction.grid(row=0, column=1, sticky="nsew")
        else:
            self.introduction.grid_forget()
        if name == "image_txt":
            self.image_txt_home.grid(row=0, column=1, sticky="nsew")
        else:
            self.image_txt_home.grid_forget()
        if name == "image_img":
            self.image_img_home.grid(row=0, column=1, sticky="nsew")
        else:
            self.image_img_home.grid_forget()
        if name == "audio_txt":
            self.audio_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.audio_frame.grid_forget()

    def introduction_stegano_button_event(self):
        self.select_frame_by_name("intro")

    def image_txt_stegano_button_event(self):
        self.select_frame_by_name("image_txt")

    def image_img_stegano_button_event(self):
        self.select_frame_by_name("image_img")

    def audio_steno_button_event(self):
        self.select_frame_by_name("audio_txt")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.override_element_colours(new_appearance_mode)    
    
    def override_element_colours(self, theme):
        # INTRO LABLE (STEALTH-STEG)
        self.navigation_frame_label.configure(text_color="black" if theme == 'Light' else 'white', bg_color="transparent", hover="white")

        # NAV ELEMENTS
        self.image_txt.configure(text_color="black" if theme == 'Light' else 'white', bg_color="#bfbfbf" if theme == 'Light' else "grey20", hover_color="#d6d2d2" if theme == 'Light' else "#1a1a1a")
        self.image_img.configure(text_color="black" if theme == 'Light' else 'white', bg_color="#bfbfbf" if theme == 'Light' else "grey20", hover_color="#d6d2d2" if theme == 'Light' else "#1a1a1a")
        self.audio_steno.configure(text_color="black" if theme == 'Light' else 'white', bg_color="#bfbfbf" if theme == 'Light' else "grey20", hover_color="#d6d2d2" if theme == 'Light' else "#1a1a1a")
        
    # IMG-TXT EMBED SECTION
    def open_txtfile(self):
        self.txt_file_path_e = customtkinter.filedialog.askopenfilename(title='Select text file', 
        # Supported file type
        filetypes=(
                ('Text files', '*.txt'),
                ('Log files', '*.log'),
                ('Configuration files', '*.conf'),
                ('Comma-separated values', '*.csv'),
                ('Tab-separated values', '*.tsv'),
                ('Extensible Markup Language', '*.xml'),
                ('Hypertext Markup Language', '*.html'),
                ('Hypertext Markup Language', '*.htm'),
                ('JavaScript Object Notation', '*.json'),
                ('YAML Ain\'t Markup Language', '*.yaml'),
                ('YAML Ain\'t Markup Language', '*.yml'),
                ('Markdown', '*.md;*.markdown'),
                ('LaTeX document', '*.latex'),
                ('LaTeX document', '*.tex'),
                ('Rich Text Format', '*.rtf')                
            )
        )
        if self.txt_file_path_e:
            with open(self.txt_file_path_e, 'r') as file:
                self.text_content = file.read()
        self.image_txt_msg_e.delete(1.0, 'end')
        self.image_txt_msg_e.insert(1.0, self.text_content)
        self.image_txt_fetch_txtfile_path_e.delete(1.0, 'end')
        self.image_txt_fetch_txtfile_path_e.insert(1.0, self.txt_file_path_e)


    # TXT-IN-IMG (EMBED SECTION)
    # ENCRYPT   
    def image_txt_embed_msg_e(self):
        self.output_path_e = self.config.get('Settings', 'txt_in_img_output_path_e')
        self.output_path_e = os.path.join(self.output_path_e, os.path.basename(self.img_file_path_e).split('.')[0])+'.png'

        try:
            #independent of class instances.
            print(self.img_file_path_e)
            self.__key_txt_in_img = txt_in_img.encrypt_image(self.img_file_path_e, self.image_txt_msg_e.get("1.0", 'end'), self.output_path_e).decode('utf-8')
            self.image_txt_output_path_e.configure(text=self.__key_txt_in_img+"\n\n"+self.output_path_e, text_color="green4")
            pyperclip.copy(self.__key_txt_in_img)
        except Exception as ve:
            self.image_txt_output_path_e.configure(text=ve, text_color="red")

    def open_imgfile_e(self):
        self.img_file_path_e = customtkinter.filedialog.askopenfilename()
        if self.img_file_path_e:
            self.new_img_e = customtkinter.CTkImage(Image.open(self.img_file_path_e), size=(165, 165))
            self.image_txt_static_imgfile_prev_e.configure(image=self.new_img_e)

    # DECRYPT  
    def open_imgfile_d(self):
        self.img_file_path_d = customtkinter.filedialog.askopenfilename()
        if self.img_file_path_d:
            self.new_img_d = customtkinter.CTkImage(Image.open(self.img_file_path_d), size=(250, 250))
            self.image_txt_static_imgfile_prev_d.configure(image=self.new_img_d)
    
    def image_txt_secret_key_dialogue_d(self):
        self.image_txt_secret_key_ask_d = customtkinter.CTkInputDialog(text="Please enter a 43-character byte string as the Fernet key to decrypt the message.\n", title="Secret Key")
        self.image_txt_secret_key_d = self.image_txt_secret_key_ask_d.get_input()

    def extract_hidden_msg_d(self):
        try:
            self.image_txt_msg_d = txt_in_img.decrypt_image(self.img_file_path_d, self.image_txt_secret_key_d)
            self.image_txt_hidden_msg_d.delete(1.0, 'end')
            self.image_txt_hidden_msg_d.insert(1.0, self.image_txt_msg_d)
        except Exception as e:
            top = customtkinter.CTkToplevel(self.image_txt_home)
            top.geometry(f"{self.screen_width//2}+{self.screen_height//2}")
            top.title("$Error$")
            customtkinter.CTkLabel(top, text= "Invalid token or image!\n Please double-check your inputs and try again.", height=150, width=380, font=customtkinter.CTkFont(size=15, weight="bold")).grid(row=0, column=0, sticky="news")
            top.lift()
            top.attributes('-topmost', True)
    # IMG-IN-IMG (EMBED SECTION)

    def open_cover_imgfile_e(self):
        self.image_img_cover_path_e = customtkinter.filedialog.askopenfilename()
        if self.image_img_cover_path_e:
            self.new_cover_img_e = customtkinter.CTkImage(Image.open(self.image_img_cover_path_e), size=(250, 250))
            self.image_img_cover_imgfile_prev_e.configure(image=self.new_cover_img_e)

    def open_secret_imgfile_e(self):
        self.image_img_secret_path_e = customtkinter.filedialog.askopenfilename()
        if self.image_img_secret_path_e:
            self.new_secret_img_e = customtkinter.CTkImage(Image.open(self.image_img_secret_path_e), size=(250, 250))
            self.image_img_secret_imgfile_prev_e.configure(image=self.new_secret_img_e)


    def image_img_embed_img_e(self):
        self.image_img_output_path_e = self.config.get('Settings', 'img_in_img_output_path_e')
        self.image_img_output_path_e = os.path.join(self.image_img_output_path_e, os.path.basename(self.image_img_cover_path_e).split('.')[0])+'.png'

        try:
            self.__key_img_in_img = img_in_img.encrypt_image(self.image_img_cover_path_e, self.image_img_secret_path_e, self.image_img_output_path_e)
            self.image_img_output_log_e.configure(text=self.__key_img_in_img + "\n\n" + self.image_img_output_path_e, text_color="green4", wraplength=580, font=customtkinter.CTkFont(size=12, weight="bold"))
            pyperclip.copy(self.__key_img_in_img)
        except ValueError as ve:
            self.image_img_output_log_e.configure(text=ve, text_color="red", wraplength=550)


    # IMG IN IMG (EXTRACT SECTION)
    def open_secret_imgfile_d(self):
        self.image_img_secret_path_d = customtkinter.filedialog.askopenfilename()
        if self.image_img_secret_path_d:
            self.new_cover_img_d = customtkinter.CTkImage(Image.open(self.image_img_secret_path_d), size=(250, 250))
            self.image_img_secret_imgfile_prev_d.configure(image=self.new_cover_img_d)
    
    def extract_hidden_img_d(self):
        self.image_img_extracted_output_path_d = self.config.get('Settings', 'img_in_img_output_path_d')
        self.image_img_extracted_output_path_d = os.path.join(self.image_img_extracted_output_path_d, os.path.basename(self.image_img_secret_path_d).split('.')[0])+'.png'
        try:
            img_in_img.decrypt_image(self.image_img_secret_path_d, self.image_img_secret_key_entry_d.get() ,self.image_img_extracted_output_path_d)
            self.new_hidden_img_d = customtkinter.CTkImage(Image.open(self.image_img_extracted_output_path_d), size=(250, 250))
            self.image_img_hidden_imgfile_prev_d.configure(image=self.new_hidden_img_d)
            self.image_img_output_path_d.configure(text=self.image_img_extracted_output_path_d, wraplength=550, text_color="green4")
        except:
            self.image_img_output_path_d.configure(text="Invalid token or image!\n Please double-check your inputs and try again.", text_color="red")

if __name__ == "__main__":
    app = App()
    app.mainloop()