class certificate:
    def __init__(self):
        file = open('certificates.txt', 'r')
        self.certificates = file.read().splitlines()
        file.close()

        self.usernames = [tuple(cert.split('|')) for cert in self.certificates]

    def verify(self, username, password):
        for user, passw in self.usernames:
            if user == username and passw == password:
                return "Certificate Verified successfully!"
            else:
                return "You need to register for certificaton!"
    
    def add(self, username, password):
        file = open('certificates.txt', 'a')
        file.write(f"{username}|{password}\n")
        file.close()
    
    def delete(self, username, password):
        file = open('certificates.txt', 'w')
            
        for ind, user, passw in enumerate(self.usernames):
            if user == username and passw == password:
                continue
            else:    
                file.write(f'\n{user}|{passw}')
        file.close()

        return "Your certificate deleted successfully!"
    
