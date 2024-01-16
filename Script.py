import fitz
import tkinter as tk
from PIL import Image, ImageTk
import os

class PDFViewer:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.current_page = 0
        self.kept_pages = []
        #initialize kept pages with everything
        for i in range(len(self.doc)):
            self.kept_pages.append(i)

        # Create main window
        self.root = tk.Tk()
        self.root.title("PDF Viewer")
        self.root.geometry("800x600")

        # Display current page
        self.image_label = tk.Label(self.root)
        self.image_label.pack(expand="true")

        # Buttons for actions

        self.label = tk.Label(self.root, text="")
        self.label.pack()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        prev_button = tk.Button(btn_frame, text="Previous", command=self.show_previous_page)
        prev_button.pack(side=tk.LEFT)

        next_button = tk.Button(btn_frame, text="Next", command=self.show_next_page)
        next_button.pack(side=tk.LEFT)

        keep_button = tk.Button(btn_frame, text="Keep", command=self.keep_current_page)
        keep_button.pack(side=tk.LEFT)

        delete_button = tk.Button(btn_frame, text="Delete", command=self.delete_current_page)
        delete_button.pack(side=tk.LEFT)

        finish_button = tk.Button(btn_frame, text="Finish", command=self.finish_and_save)
        finish_button.pack(side=tk.LEFT)

        # Bind keys to functions
        self.root.bind('<Return>', lambda event: self.delete_current_page())
        self.root.bind('<space>', lambda event: self.keep_current_page())
        self.root.bind('<Left>', lambda event: self.show_previous_page())
        self.root.bind('<Right>', lambda event: self.show_next_page())


        # Display the first page
        self.show_current_page()

    def show_current_page(self):

        if self.current_page in self.kept_pages:
            self.label.config(text="Kept")
        else:
            self.label.config(text="Deleted")
        self.root.update()

        page = self.doc.load_page(self.current_page)
        pix = page.get_pixmap()

        # Adjust the scaling factor as needed
        scaling_factor = 1.5

        # Convert Pixmap to Image and scale
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = img.resize((int(img.width * scaling_factor), int(img.height * scaling_factor)), Image.ANTIALIAS)

        # Convert Image to PhotoImage
        img_tk = ImageTk.PhotoImage(image=img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def show_next_page(self):
        if self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.show_current_page()

    def keep_current_page(self):
        self.kept_pages.append(self.current_page)
        self.show_next_page()

    def delete_current_page(self):
        #remove from kept
        if self.current_page in self.kept_pages:
            self.kept_pages.remove(self.current_page)
        self.show_next_page()

    def finish_and_save(self):
        # Create a new PDF with only the kept pages
        new_doc = fitz.open()

        # Iterate through all pages of the original PDF
        for page_num in range(len(self.doc)):
            # Insert the page if it was not explicitly kept
            if page_num in self.kept_pages:
                new_doc.insert_pdf(self.doc, from_page=page_num, to_page=page_num)

        # Save the new PDF
        output_path = os.path.splitext(self.pdf_path)[0] + "_edited.pdf"
        new_doc.save(output_path)
        new_doc.close()

        # Close the original PDF
        self.doc.close()

        # Destroy the application window
        self.root.destroy()


if __name__ == "__main__":
    pdf_path = ""  # Replace with the path to your PDF file
    pdf_viewer = PDFViewer(pdf_path)
    pdf_viewer.root.mainloop()

