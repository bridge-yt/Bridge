openssl genrsa -out key.pem 2048
openssl req -new -key key.pem -out csr.pem -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"
openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem
rm csr.pem
