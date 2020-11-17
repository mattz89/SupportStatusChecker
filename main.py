import tkinter as tk
from selenium import webdriver
import chromedriver_binary
from datetime import *
from PIL import Image


WIDTH = 1200
HEIGHT = 1000


def support_checker(lic):
    # configure headless chrome + selenium
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=850x950')
    driver = webdriver.Chrome(chrome_options = options)

    # Open to KW
    driver.get('https://www.kioware.com/partners.aspx')
    driver.implicitly_wait(30)

    # Get login elements
    email = driver.find_element_by_id('ctl00_CPH_RightCol_tb_Partneremail')
    password = driver.find_element_by_id('ctl00_CPH_RightCol_tb_partnerPW')
    login = driver.find_element_by_id('ctl00_CPH_RightCol_btn_continue1')

    # Perform login
    email.send_keys('')
    password.send_keys('')
    login.click()

    # Navigate to company page
    driver.get('https://www.kioware.com/partners.aspx?m=company')

    # Perform search with license transaction number
    search_field = driver.find_element_by_id('ctl00_CPH_MainContent_ADSI_Company_Editor1_tbSearchTerms')
    transaction_selector = driver.find_element_by_id('licensetransactionnumber')
    transaction_selector.click()
    search_field.send_keys(lic)

    # Get company details and navigate to company page
    company_id = driver.find_element_by_css_selector('td[class=CompanyID]').text
    master_id = driver.find_element_by_css_selector('td[class=MasterID]').text
    driver.get(f'https://www.kioware.com/partners.aspx?m=company&coid={company_id}&masid={master_id}')

    # Navigate to support renewal page
    renew_support = driver.find_element_by_id('ctl00_CPH_MainContent_ADSI_Company_Editor1_btn_renewsupport')
    renew_support.click()

    # Compare support end date to today's date
    support_ends = driver.find_element_by_id('ctl00_CPH_MainContent_ADSI_Company_Editor1_SupportRenewPackageViewer1_lbSupportEndsOn').text
    support_ends_convert = datetime.strptime(support_ends, '%m/%d/%Y')
    today = datetime.now()

    if support_ends_convert > today:
        support_status = 'Support is current'
    else:
        support_status = 'Support is not current'
    
    print(support_status)

    # Screenshot and crop support renewal information 
    driver.get_screenshot_as_file('support.png')
    im = Image.open('support.png')
    im_crop = im.crop((0, 490, 800, 950))
    im_crop.save('support.png')

    results['text'] = support_status
    support_image['file'] = 'support.png'


root = tk.Tk()

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
canvas.pack()

# Header frame for logo
header_frame = tk.Frame(root)
header_frame.place(relx=0.5, rely=0.05, relwidth=0.8, relheight=0.1, anchor='n')

# Logo insert to header frame
logo = tk.PhotoImage(file='kwlogo.png')
logo_pack = tk.Label(header_frame, image=logo, bg='black')
logo_pack.place(relwidth=1, relheight=1)

# Create top frame for input
input_frame = tk.Frame(root, bg='#1589FF', bd=5)
input_frame.place(relx=0.5, rely=0.15, relwidth=0.8, relheight=0.1, anchor='n')

# Field for license transaction number
lic = tk.Entry(input_frame, font=60, bg='#2B3856', fg='#FFFFFF')
lic.place(relwidth=0.65, relheight=1)

# Button for checking support
check_support = tk.Button(input_frame, text="Check Support", font=60, command=lambda: support_checker(lic.get()))
check_support.place(relx=0.7, relheight=1, relwidth=0.3)

# Create bottom frame for results
results_frame = tk.Frame(root, bg='#1589FF', bd=5)
results_frame.place(relx=0.5, rely=0.27, relwidth=0.8, relheight=0.7, anchor='n')

# Label to house results
results = tk.Label(results_frame, font=60, bg='#2B3856', fg='#FFFFFF')
results.place(relwidth=1, relheight=0.2)

# Embed support image
support_image = tk.PhotoImage()
support_image_pack = tk.Label(results_frame, image=support_image, bg='#2B3856')
support_image_pack.place(rely=0.2, relwidth=1, relheight=0.8)

# End GUI loop
root.mainloop()