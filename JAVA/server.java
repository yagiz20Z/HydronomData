import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Arrays;

public class Server {

    public static void main(String[] args) {
        int PORT = 45000;

        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("SERVER başlatıldı → Port: " + PORT);

            while (true) {
                Socket client = serverSocket.accept();
                System.out.println("CLIENT bağlandı: " + client.getInetAddress());

                InputStream in = client.getInputStream();

                while (true) {
                    int header = in.read();
                    if (header == -1) break;      // bağlantı kapandı
                    if (header != 0xAA) continue; // header değilse veri atla

                    int length = in.read();       // payload uzunluğu
                    if (length == -1) break;

                    byte[] payload = in.readNBytes(length);
                    int checksum = in.read();

                    // Checksum hesapla
                    int calculated = 0;
                    for (byte b : payload)
                        calculated ^= b;

                    if (checksum == calculated) {
                        System.out.println("Packet OK → DATA: " + Arrays.toString(payload));
                    } else {
                        System.out.println("Checksum ERROR!");
                    }
                }
            }

        } catch (Exception e) {
            System.err.println("Server hatası: " + e.getMessage());
        }
    }
}
