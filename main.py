import os
import tkinter as tk
from xml.etree import ElementTree as ET
from PIL import Image, ImageTk


class BookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kitap Arayüzü")

        # Kitap verilerini saklamak için bir liste
        self.books = self.parse_xml("veriSeti.xml")

        # Başlık
        self.label = tk.Label(root, text="Buse'nin Kitap Arşivi", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Liste kutusu
        self.listbox = tk.Listbox(root)
        for book in self.books:
            self.listbox.insert(tk.END, book["dcTitle"])
        self.listbox.pack(pady=10)

        # Detay gösterme butonu
        self.show_button = tk.Button(root, text="Detayları Göster", command=self.show_details)
        self.show_button.pack(pady=5)

        # Çıkış butonu
        self.exit_button = tk.Button(root, text="Çıkış", command=root.destroy)
        self.exit_button.pack(pady=5)

    def parse_xml(self, file_path):
        books = []
        tree = ET.parse(file_path)
        root = tree.getroot()
        for book_elem in root.findall("eser"):
            book = {}
            for child_elem in book_elem:
                if child_elem.tag == "dcImage":
                    # Dosya adındaki tek tırnak ve boşluğu düzelt
                    image_filename = f"{book_elem.find('dcTitle').text.lower().replace(' ', '_')}.jpg"
                    book[child_elem.tag] = os.path.join("image", image_filename)
                else:
                    book[child_elem.tag] = child_elem.text
            books.append(book)
        return books

    def show_details(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_book = self.books[selected_index]

            # Detay penceresi
            detail_window = tk.Toplevel(self.root)
            detail_window.title(selected_book["dcTitle"])

            # Kitap detayları
            detail_label = tk.Label(detail_window, text=f"{selected_book['dcTitle']} - {selected_book['dcCreator']}")
            detail_label.pack(pady=10)

            # Kitap açıklaması
            description_label = tk.Label(detail_window, text=selected_book['dcDescription'], wraplength=400,
                                         justify="left")
            description_label.pack(pady=10)

            # Diğer bilgiler
            subject_label = tk.Label(detail_window, text=f"Subject: {selected_book['dcSubject']}")
            subject_label.pack(pady=5)

            creator_label = tk.Label(detail_window, text=f"Creator: {selected_book['dcCreator']}")
            creator_label.pack(pady=5)

            contributor_label = tk.Label(detail_window, text=f"Contributor: {selected_book['dcContributor']}")
            contributor_label.pack(pady=5)

            language_label = tk.Label(detail_window, text=f"Language: {selected_book['dcLanguage']}")
            language_label.pack(pady=5)

            identifier_label = tk.Label(detail_window, text=f"Identifier: {selected_book['dcIdentifier']}")
            identifier_label.pack(pady=5)

            # Kitap görseli
            image_path = selected_book['dcImage']
            image_file = Image.open(image_path)
            image_resized = image_file.resize((150, 200), Image.ANTIALIAS)
            image_tk = ImageTk.PhotoImage(image_resized)

            image_label = tk.Label(detail_window, image=image_tk)
            image_label.image = image_tk  # Referansı tutmak önemlidir
            image_label.pack(pady=10)


# Ana uygulama penceresini oluştur
root = tk.Tk()
app = BookApp(root)
root.mainloop()
