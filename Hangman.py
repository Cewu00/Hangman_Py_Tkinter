import tkinter as tk
from tkinter import ttk
from random import randint
from os.path import isfile, getsize, join
from pygame import mixer


BIG_BUTTON_FONT = ('Lato',28)
BUTTON_FONT = ('Lato', 16)
TITLE_FONT = ('Copperplate Gothic Bold', 38)
BOARD_FONT = ('Arial', 15)

PopUpMessageBox_status = False
name_input_box_status = False

def play_sound_effect(file_name):
        folder_path = 'Sounds'

        mixer.init()
        sound_effect = mixer.Sound(join(folder_path, file_name))
        mixer.Sound.play(sound_effect)

class NameInputBox_HangMan(tk.Toplevel):
	name_input_box_status = False

	entry1_value = 'empty'
	def __init__(self, controller, parent, text):

		self.controller = controller
		
		if self.name_input_box_status == False:
			tk.Toplevel.__init__(self, parent)
			self.name_input_box_status = True

			self.wm_title("Input Name.")

			self.label_message = tk.Label(self, text = text, font = (BUTTON_FONT, 20))

			self.frame1 = ttk.Frame(self)
			self.entry1 = ttk.Entry(self.frame1, font = BUTTON_FONT, width = 10)
			self.button_message = ttk.Button(self.frame1, text="Ok", command = lambda: self.name_input_box_exit())
			
			self.entry1.pack(side = 'left', padx = 5, pady = 5)
			self.button_message.pack(side = 'left', pady = 5, padx = 5)

			self.label_message.pack(side = 'top', pady = 10, padx = 10)
			self.frame1.pack(side = 'bottom', pady = 10, padx = 10)

			#TODO: Valjalo bi da se otvara na sred glavnog prozora
		else: 
			pass

	def name_input_box_exit(self):
		page1 = self.controller.get_page(GamePage_HangMan)
		page2 = self.controller.get_page(LeaderboardPage_HangMan)
		self.name_input_box_status = False
		
		self.name = self.entry1.get()
		self.entry1.delete(0,tk.END)

		self.win = page1.win
		self.loss = page1.loss

		page2.write_to_leaderboard(self.name, self.win, self.loss)

		self.destroy()


def PopUpMessageBox(text):
	global PopUpMessageBox_status

	if PopUpMessageBox_status == False:
		PopUpMessageBox_status = True
		window = tk.Toplevel()
		window.wm_title("Input Error!")

		label_message = tk.Label(window, text = text, font = (BUTTON_FONT, 20))
		label_message.pack(side = 'top', pady = 10, padx = 10)

		button_message = ttk.Button(window, text="Ok", command = lambda: PopUpMessageBox_exit(window))
		button_message.pack(side = 'bottom', pady = 10)
		return
		#TODO: Valjalo bi da se otvara na sred glavnog prozora
	else: 
		return

def PopUpMessageBox_exit(window):
	global PopUpMessageBox_status
	PopUpMessageBox_status = False
	window.destroy()
	return


class MultiPage(tk.Tk):

	image_height = 500
	image_width = 600

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)

		self.HxW = str(MultiPage.image_width)+'x'+str(MultiPage.image_height)
		self.geometry(self.HxW)
		self.maxsize(MultiPage.image_width,MultiPage.image_height)
		self.minsize(MultiPage.image_width,MultiPage.image_height)
		self.title('Pogodi Zemlju')

		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand = True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (MainMenu_HangMan, GamePage_HangMan, LeaderboardPage_HangMan, GameMenuPage_HangMan):

			frame = F(parent = container, controller = self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(MainMenu_HangMan)
		
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

	def get_page(self, page_class):
		return self.frames[page_class]

	def close_window(self):
		LeaderboardPage_HangMan.Lista_Igraca.close() # closes leaderboard storage file
		self.quit() # tkinter break main loop function
		exit() # python kill funciton


class MainMenu_HangMan(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.controller=controller

		self.bg = tk.PhotoImage(file='Images/space.png')
		self.background_canvas = tk.Canvas(self, width = 600, height=500)
		self.background_canvas.pack(fill="both", expand=True)
		self.background_canvas.create_image(0,0, image=self.bg, anchor='nw')

		self.label1 = tk.Label(self.background_canvas, text='Hangman', font = TITLE_FONT, bg = 'black', fg = 'white')

		self.button1 = tk.Button(self.background_canvas, text = 'Start Game', font = BIG_BUTTON_FONT, width=10, command = lambda: self.button1_f(controller))
		self.button2 = tk.Button(self.background_canvas, text = 'Leaderboard', font = BIG_BUTTON_FONT, width=10, command = lambda: self.button2_f(controller))
		self.button3 = tk.Button(self.background_canvas, text = 'Quit', font = BIG_BUTTON_FONT, width=10, command = lambda: controller.close_window())

		self.background_canvas.pack(side='top')
		self.label1.pack(side='top', pady = 20)
		self.button1.pack(side='top', pady=40)
		self.button2.pack(side='top', pady=0)
		self.button3.pack(side='top', pady=40)

	def button1_f(self, controller):
		controller.show_frame(GamePage_HangMan)
		page = self.controller.get_page(GamePage_HangMan)

		num_lines = page.check_list_refresh()
		page.configure_word_show(page.word_setting(page.word_choice(num_lines)))
		page.mistake_tracking = 0
		page.hang_man_image_update(page.mistake_tracking)
		page.win = 0
		page.loss = 0
		page.game_ended = False
		page.frame2.place_forget()
		
	def button2_f(self, controller):
		controller.show_frame(LeaderboardPage_HangMan)
		page = self.controller.get_page(LeaderboardPage_HangMan)

		Lista_Igraca = open('Lista_Igraca_HangMan.txt', 'r') 

		igrac = Lista_Igraca.readline()

		counter1 = 0
		Igraci_Printout = []

		while counter1 != 9:
			igrac = igrac[:-1]
			Igraci_Printout.append(igrac)
			counter1 += 1
			if counter1 == 9:
				break	
			igrac = Lista_Igraca.readline()
			if igrac == '':
				while counter1 != 9:
					Igraci_Printout.append('')
					counter1 += 1
		Lista_Igraca.close()

		page.br_stranice = 0

		page.configure_leaderboard(Igraci_Printout)
		page.create_leaderboard()


class LeaderboardPage_HangMan(tk.Frame):

	if not isfile('Lista_Igraca_HangMan.txt'):
		Lista_Igraca = open('Lista_Igraca_HangMan.txt', 'x')
		Lista_Igraca.close()

	Lista_Igraca = open('Lista_Igraca_HangMan.txt', 'r')

	br_stranice = 0
	marker = []
	igrac_class = 'place_hoder'
	num_igraca_class = 0

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.controller = controller

		# Makes Background
		self.bg = tk.PhotoImage(file='Images/space.png')
		self.background_canvas = tk.Canvas(self, width = 600, height=500)
		self.background_canvas.pack(fill="both", expand=True)
		self.background_canvas.create_image(0,0, image=self.bg, anchor='nw')

		self.create_leaderboard()
		
		# Title
		self.title = tk.Label(self.background_canvas, text="Leaderboard", font = TITLE_FONT, bg = 'black', fg = 'white')

		# Leaderboard
		self.board0 = tk.Label(self.background_canvas, text = 'Position\t   Name\t  Wins\tLosses', font = BOARD_FONT, bg = 'black', fg = 'white')
		self.board1 = tk.Label(self.background_canvas, text = '', font = BOARD_FONT, bg = 'black', fg = 'white')
		self.board2 = tk.Label(self.background_canvas, text = '', font = BOARD_FONT, bg = 'black', fg = 'white')
		self.board3 = tk.Label(self.background_canvas, text = '', font = BOARD_FONT, bg = 'black', fg = 'white')
		self.board4 = tk.Label(self.background_canvas, text = '', font = BOARD_FONT, bg = 'black', fg = 'white')
		self.board5 = tk.Label(self.background_canvas, text = '', font = BOARD_FONT, bg = 'black', fg = 'white')
		self.board6 = tk.Label(self.background_canvas, text = '', font = BOARD_FONT, bg = 'black', fg = 'white')
		self.board7 = tk.Label(self.background_canvas, text = '', font = BOARD_FONT, bg = 'black', fg = 'white')
		self.board8 = tk.Label(self.background_canvas, text = '', font = BOARD_FONT, bg = 'black', fg = 'white')
		self.board9 = tk.Label(self.background_canvas, text = '', font = BOARD_FONT, bg = 'black', fg = 'white')

		# Buttons Frame
		self.frame1 = tk.Frame(self.background_canvas, bg = 'black', bd = 0)

		self.button1 = tk.Button(self.frame1, text = 'Next', font = BUTTON_FONT, command = lambda: self.next_page())
		self.button2 = tk.Button(self.frame1, text = 'Exit', font = BUTTON_FONT, command = lambda: self.exit_leaderboard(controller)) 
		self.button3 = tk.Button(self.frame1, text = 'Prev', font = BUTTON_FONT, command = lambda: self.previous_page())
			
		self.button1.pack(side = 'right')
		self.button2.pack(side = 'right', padx = 20)
		self.button3.pack(side = 'right')

		# GUI PLACMENT:
		self.background_canvas.pack(side='top')

		self.title.pack(side = 'top', pady = 20)

		self.board0.pack(side = 'top', anchor = 'n')
		self.board1.pack(side = 'top', anchor = 'n')
		self.board2.pack(side = 'top', anchor = 'n')
		self.board3.pack(side = 'top', anchor = 'n')
		self.board4.pack(side = 'top', anchor = 'n')
		self.board5.pack(side = 'top', anchor = 'n')
		self.board6.pack(side = 'top', anchor = 'n')
		self.board7.pack(side = 'top', anchor = 'n')
		self.board8.pack(side = 'top', anchor = 'n')
		self.board9.pack(side = 'top', anchor = 'n')
		
		self.frame1.pack(side = 'bottom', pady = 30)


	def exit_leaderboard(self, controller):
		controller.show_frame(MainMenu_HangMan)

	def create_leaderboard(self):
		if self.Lista_Igraca.tell() not in self.marker:
			self.marker.append(self.Lista_Igraca.tell())

		if self.br_stranice == 0:
			self.Lista_Igraca.seek(0)

		igrac = self.Lista_Igraca.readline()
		counter1 = 0
		Igraci_Printout = []
		while counter1 != 9:
			igrac = igrac[:-1]
			Igraci_Printout.append(igrac)
			counter1 += 1
			if counter1 == 9:
				break	
			igrac = self.Lista_Igraca.readline()
			if igrac == '':
				while counter1 != 9:
					Igraci_Printout.append('')
					counter1 += 1

		self.igrac_class = igrac

		self.Counting_Players = open('Lista_Igraca_HangMan.txt', 'r')
		num_igraca = sum(1 for line in self.Counting_Players)
		self.Counting_Players.close() 
		self.num_igraca_class = num_igraca

		return Igraci_Printout

	def configure_leaderboard(self, Igraci_Printout):
		self.board1.config(text = Igraci_Printout[0])
		self.board2.config(text = Igraci_Printout[1])
		self.board3.config(text = Igraci_Printout[2])
		self.board4.config(text = Igraci_Printout[3])
		self.board5.config(text = Igraci_Printout[4])
		self.board6.config(text = Igraci_Printout[5])
		self.board7.config(text = Igraci_Printout[6])
		self.board8.config(text = Igraci_Printout[7])
		self.board9.config(text = Igraci_Printout[8])

	def previous_page(self):
		if not(self.br_stranice == 0 
			or self.num_igraca_class < 9 
			or getsize('Lista_Igraca_HangMan.txt') == 0):

			self.br_stranice -= 1
			self.Lista_Igraca.seek(self.marker[self.br_stranice]) 
			self.configure_leaderboard(self.create_leaderboard())
			return True

		else: 
			return False
		
	def next_page(self):
		if not(self.igrac_class == '' 
			or self.num_igraca_class < 9 
			or getsize('Lista_Igraca_HangMan.txt') == 0 
			or ((self.br_stranice+1) * 9 == self.num_igraca_class)):

			self.br_stranice += 1
			self.configure_leaderboard(self.create_leaderboard())

	def write_to_leaderboard(self, name, wins, losses): 

		if not isfile('Lista_Igraca_HangMan.txt'):
			Lista_Igraca = open('Lista_Igraca_HangMan.txt', 'x')
			Lista_Igraca.close()
		
		Lista_Igraca = open('Lista_Igraca_HangMan.txt', 'r')
		num_igraca = sum(1 for line in Lista_Igraca)
		Lista_Igraca.close() 

		if getsize('Lista_Igraca_HangMan.txt') == 0:
			fajl_unos = str(f'{1}.\t{name}\t{wins}\t{losses}\n')
		else:
			fajl_unos = str(f'{num_igraca+1}.\t{name}\t{wins}\t{losses}\n')
		
		Lista_Igraca = open('Lista_Igraca_HangMan.txt', "a")
		Lista_Igraca.write(str(fajl_unos))
		Lista_Igraca.close()

		player_list = []
		fajl_list = open('Lista_Igraca_HangMan.txt', 'r')
		for line in fajl_list:
			player_list.append(line)
		fajl_list.close()

		self.insertionSort_hangman(player_list, self.scoreify_hangman(player_list))

		for i in range(len(player_list)):
			count = 0
			for letter in player_list[i]:
				if letter >= '0' and letter <= '9':
					count += 1
				elif letter == '.':
					# pom = str()
					player_list[i] = player_list[i].replace(player_list[i][:count], str(i+1), 1)
					break

		Lista = open('Lista_Igraca_HangMan.txt', 'w')
		for row in player_list:
			Lista.write(row)
		Lista.close()

		self.marker = []
		self.Lista_Igraca.seek(0)

		self.num_igraca_class += 1


	def scoreify_hangman(self, player_list):
		score_list = []

		for row in player_list:
			count = 0
			suma = 0
			row_number = 0

			for i in range(len(row)-2, 0, -1):
				if row[i] == '\t':
					count += 1
					row_number = 0
				elif count == 0: 
					suma -= (10**row_number * int(row[i]))
					row_number += 1
				elif count == 1:
					suma += 2*(10**row_number *int(row[i]))
					row_number += 1
				elif count == 2:
					score_list.append(suma)
					break

		return score_list

	def insertionSort_hangman(self, lista_igraca, score_list):
		
		for i in range(1, len(score_list)):

			key1 = score_list[i]
			key2 = lista_igraca[i]

			j = i-1
			while j >=0 and key1 > score_list[j] :
				score_list[j+1] = score_list[j]
				lista_igraca[j+1] = lista_igraca[j]
				j -= 1

			score_list[j+1] = key1
			lista_igraca[j+1] = key2
		

class GameMenuPage_HangMan(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller=controller

		self.background_canvas = tk.Canvas(self, bg = 'black')

		self.label1 = tk.Label(self.background_canvas, text='Menu', font = TITLE_FONT, bg = 'black', fg = 'white')

		self.button1 = tk.Button(self.background_canvas, text = 'Continue', font = BIG_BUTTON_FONT, width=11, command = lambda: controller.show_frame(GamePage_HangMan))
		self.button2 = tk.Button(self.background_canvas, text = 'Restart Game', font = BIG_BUTTON_FONT, width=11, command = lambda: self.restart_button(controller))
		self.button3 = tk.Button(self.background_canvas, text = 'Exit & Save', font = BIG_BUTTON_FONT, width=11, command = lambda: self.exit_save())
		self.button4 = tk.Button(self.background_canvas, text = 'Exit Game', font = BIG_BUTTON_FONT, width=11, command = lambda: controller.show_frame(MainMenu_HangMan))

		self.background_canvas.pack(side='top', fill="both", expand=True)
		self.label1.pack(side='top', pady = 15)

		self.button1.pack(side='top', pady = 10)
		self.button2.pack(side='top', pady = 10)
		self.button3.pack(side='top', pady = 10)
		self.button4.pack(side='top', pady = 10)

	def restart_button(self, controller):
		page = self.controller.get_page(MainMenu_HangMan)
		page.button1_f(controller)

	def exit_save(self):
		page = self.controller.get_page(GamePage_HangMan)
		page.exit_save()

	
class GamePage_HangMan(tk.Frame):

	word_class = ''
	file_len_Lista_Zemalja = 0 
	num_lines_class = -1
	mistake_tracking = 0
	output_class = None
	win = 0
	loss = 0

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.parent = parent

		self.hang_man_paths = []
		self.hang_man_images = []
		for i in range(0,8):
			self.hang_man_images.append(tk.PhotoImage(file = f'Images/hang_man #{i}.png'))

		self.game_ended = False

		self.file_len_Lista_Zemalja = getsize('Word_List.txt')
		self.first_time_clicked_detector = True

		self.bg = tk.PhotoImage(file='Images/space.png')
		self.background_canvas = tk.Canvas(self, width = 600, height=500)
		self.background_canvas.pack(fill="both", expand=True)
		self.background_canvas.create_image(0,0, image=self.bg, anchor='nw')

		self.hang_man_canvas = tk.Canvas(self.background_canvas, width = 137, height = 167, bg = 'black', highlightthickness=0, relief='ridge')
		self.hang_man_on_canvas = self.hang_man_canvas.create_image(0, 0, image = self.hang_man_images[self.mistake_tracking], anchor = 'nw')

		self.label2 = tk.Label(self.background_canvas, text = self.word_class, font = ('Lato', 24), bg = 'black', fg = 'white')
		
		self.frame1 = tk.Frame(self.background_canvas, bg = 'black')
		self.entry1 = tk.Entry(self.frame1, font = BOARD_FONT)
		self.button_input = tk.Button(self.frame1, text = 'OK', font = BUTTON_FONT, command = self.game_logic)

		self.entry1.pack(side = 'left', pady = 10)
		self.button_input.pack(side = 'left', pady = 10)

		self.controller.bind('<Return>', lambda event: self.game_logic())

		self.button1 = tk.Button(self.background_canvas, text ="Quit Game", font = BUTTON_FONT, command = lambda: controller.show_frame(GameMenuPage_HangMan))

		self.frame2 = tk.Frame(self.background_canvas, bg = 'black')
		self.button_newgame = tk.Button(self.frame2, text = 'New Game', font = BUTTON_FONT, width = 10, command = lambda: self.new_game())
		self.button_exitsave = tk.Button(self.frame2, text = 'Exit & Save', font = BUTTON_FONT, width = 10, command = lambda: self.exit_save())
		self.button_exit = tk.Button(self.frame2, text = 'Exit', font = BUTTON_FONT, width = 10, command = lambda: controller.show_frame(MainMenu_HangMan))
		
		self.button_newgame.pack(side = 'top', pady = 0)
		self.button_exitsave.pack(side = 'top', pady = 20)
		self.button_exit.pack(side = 'top', pady = 0)

		self.background_canvas.pack(side = 'top')
		self.hang_man_canvas.place(anchor = 'nw', x = 75, y = 30)
		
		self.button1.pack(side = 'bottom', pady = 25)
		self.frame1.pack(side = 'bottom', pady = 30)
		self.label2.pack(side = 'bottom', pady = 5)

	def new_game(self):
		num_lines = self.check_list_refresh()
		self.configure_word_show(self.word_setting(self.word_choice(num_lines)))
		self.hang_man_image_update(self.mistake_tracking)
		self.frame2.place_forget()
		self.game_ended = False

	def exit_save(self):
		name_box = NameInputBox_HangMan(self.controller, self.parent, 'Input the Name:') 
		self.controller.show_frame(MainMenu_HangMan)
	
	def hang_man_image_update(self, number):
		if number <= 7:
			self.hang_man_canvas.itemconfig(self.hang_man_on_canvas, image = self.hang_man_images[number])

	def game_logic(self):

		if self.game_ended == True:
			self.entry1.delete(0,tk.END)
			return

		char = str(self.entry1.get()).upper()
		self.entry1.delete(0,tk.END)

		if len(char) != 1 or (char < 'A' or char > 'Z'):
			PopUpMessageBox('You must input one letter only!')
			return
		
		if char in self.word_class.upper():
			for i in range(len(self.word_class)):
				if char == self.word_class[i].upper():
					self.word_print_class = list(self.word_print_class)
					self.word_print_class[i] = self.word_class[i]
					
			output = ''.join(self.word_print_class)
			self.output_class = output
			self.configure_word_show(output)
		else:
			self.mistake_tracking += 1
			self.hang_man_image_update(self.mistake_tracking)

		if self.mistake_tracking == 7:
			self.loss += 1
			self.hang_man_image_update(self.mistake_tracking)
			self.mistake_tracking = 0
			self.configure_word_show('You Lose!')
			self.frame2.place(anchor = 'nw', x = 400, y = 30)
			self.game_ended = True
			play_sound_effect('hangman_loss.mp3')
			return	
			
		elif self.output_class == self.word_class:
			self.win += 1
			self.mistake_tracking = 0
			self.configure_word_show('You Win!')
			self.frame2.place(anchor = 'nw', x = 400, y = 30)
			self.game_ended = True
			play_sound_effect('hangman_win.mp3')
			return	
			
			# TODO: Optimise calling similar sets of functions on button_clicks

			# TODO: Explain the inner workings of the program through comments

			# TODO: Maybe add functionality for tracking used letters and have them display in a corner...
			# TODO: Inputting whole words, requires exact word or you die :)

	def word_choice(self, num_lines):
		Countries = open('Word_List.txt', 'r') # This file has to exist. TODO: add a check

		number = randint(0, num_lines)
		#number = 183 # The biggest word that is in the list of countries, useful to test if everything is displayed correctly
		word = ''
		i = 0
		for f in Countries: #Picking a random word
			if i == number:
				word = f[:-1] #mora f[:-1] kako bi makli '\n' sa kraja
				break
			i+=1

		Countries.close()
		self.word_class = word 
		return word

	def word_setting(self, word):
		#pravi ---- --- sa razmacima
		word_guess = []
		for j in word:
			if j == ' ':
				word_guess.append(' ')
			else:
				word_guess.append('-')   
		word_print = ''.join(word_guess)

		self.word_print_class = word_print
		return word_print

	def configure_word_show(self, word):
		self.label2.config(text = word)

	def check_list_refresh(self):
		if self.file_len_Lista_Zemalja != getsize('Word_List.txt') or self.first_time_clicked_detector == True:
			Zemlje = open('Word_List.txt', 'r')
			num_lines = sum(1 for line in Zemlje)
			Zemlje.close() #line count

			self.num_lines_class = num_lines
			self.first_time_clicked_detector = False
			self.file_len_Lista_Zemalja = getsize('Word_List.txt')

		try: 
			return num_lines
		except UnboundLocalError:
			return self.num_lines_class
			


















app = MultiPage()
app.mainloop()

		
		







