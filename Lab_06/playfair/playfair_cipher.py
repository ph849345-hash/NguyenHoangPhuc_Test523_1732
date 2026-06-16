class PlayFairCipher:
    
    def __init__(self):
        pass

    # =========================
    # TẠO MA TRẬN PLAYFAIR
    # =========================
    def create_playfair_matrix(self, key):

        # Chuyển J -> I
        key = key.replace("J", "I")
        key = key.upper()

        # Loại ký tự trùng
        new_key = ""

        for char in key:
            if char.isalpha() and char not in new_key:
                new_key += char

        # Alphabet bỏ J
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

        matrix = list(new_key)

        # Thêm ký tự còn thiếu
        for letter in alphabet:
            if letter not in matrix:
                matrix.append(letter)

        # Chỉ lấy 25 phần tử
        matrix = matrix[:25]

        # Chia thành ma trận 5x5
        playfair_matrix = [
            matrix[i:i+5]
            for i in range(0, 25, 5)
        ]

        return playfair_matrix

    # =========================
    # TÌM TỌA ĐỘ KÝ TỰ
    # =========================
    def find_letter_coords(self, matrix, letter):

        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col

        return None

    # =========================
    # CHUẨN HÓA PLAINTEXT
    # =========================
    def prepare_plain_text(self, plain_text):

        plain_text = plain_text.replace("J", "I")
        plain_text = plain_text.upper()

        # Xóa khoảng trắng
        plain_text = plain_text.replace(" ", "")

        prepared_text = ""

        i = 0

        while i < len(plain_text):

            char1 = plain_text[i]

            if i + 1 < len(plain_text):

                char2 = plain_text[i + 1]

                # Nếu 2 ký tự giống nhau
                if char1 == char2:

                    prepared_text += char1 + "X"
                    i += 1

                else:

                    prepared_text += char1 + char2
                    i += 2

            else:

                # Nếu còn 1 ký tự
                prepared_text += char1 + "X"
                i += 1

        return prepared_text

    # =========================
    # ENCRYPT
    # =========================
    def playfair_encrypt(self, plain_text, matrix):

        # Chuẩn hóa plaintext
        plain_text = self.prepare_plain_text(plain_text)

        encrypted_text = ""

        for i in range(0, len(plain_text), 2):

            pair = plain_text[i:i+2]

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            # Cùng hàng
            if row1 == row2:

                encrypted_text += (
                    matrix[row1][(col1 + 1) % 5] +
                    matrix[row2][(col2 + 1) % 5]
                )

            # Cùng cột
            elif col1 == col2:

                encrypted_text += (
                    matrix[(row1 + 1) % 5][col1] +
                    matrix[(row2 + 1) % 5][col2]
                )

            # Hình chữ nhật
            else:

                encrypted_text += (
                    matrix[row1][col2] +
                    matrix[row2][col1]
                )

        return encrypted_text

    # =========================
    # DECRYPT
    # =========================
    def playfair_decrypt(self, cipher_text, matrix):

        cipher_text = cipher_text.upper()

        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):

            pair = cipher_text[i:i+2]

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            # Cùng hàng
            if row1 == row2:

                decrypted_text += (
                    matrix[row1][(col1 - 1) % 5] +
                    matrix[row2][(col2 - 1) % 5]
                )

            # Cùng cột
            elif col1 == col2:

                decrypted_text += (
                    matrix[(row1 - 1) % 5][col1] +
                    matrix[(row2 - 1) % 5][col2]
                )

            # Hình chữ nhật
            else:

                decrypted_text += (
                    matrix[row1][col2] +
                    matrix[row2][col1]
                )

        # Xóa X được chèn thêm
        final_text = ""

        i = 0

        while i < len(decrypted_text):

            # Trường hợp AXA -> AA
            if (
                i + 2 < len(decrypted_text)
                and decrypted_text[i] == decrypted_text[i + 2]
                and decrypted_text[i + 1] == "X"
            ):

                final_text += decrypted_text[i]
                i += 2

            else:

                final_text += decrypted_text[i]
                i += 1

        # Xóa X cuối nếu có
        if final_text.endswith("X"):
            final_text = final_text[:-1]

        return final_text