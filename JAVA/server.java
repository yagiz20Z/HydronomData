import java.io.*;
import java.net.*;
import com.fazecast.jSerialComm.SerialPort; // jSerialComm kütüphanesini import et

public class server {

    private static final int BUFFER_SIZE = 1024;
    private static final int TIMEOUT = 30000; // 30 saniye

    // --- YENİ ---
    private static SerialPort stm32Port;
    private static final String STM32_COM_PORT = "COM3"; // STM32'nizin bağlandığı port (Windows'ta)
    // Linux'ta /dev/ttyUSB0 gibi
    private static final int STM32_BAUD_RATE = 115200;  // STM32'deki ile aynı olmalı
    // --- YENİ BİTİŞ ---

    public static void main(String[] args) {
        int PORT = 45000;

        // --- YENİ: Seri Portu Başlat ---
        stm32Port = SerialPort.getCommPort(STM32_COM_PORT);
        stm32Port.setBaudRate(STM32_BAUD_RATE);

        if (!stm32Port.openPort()) {
            System.err.println("Seri port açılamadı: " + STM32_COM_PORT);
            return; // Port açılamazsa programdan çık
        }
        System.out.println("STM32 seri portu (" + STM32_COM_PORT + ") açıldı.");
        // --- YENİ BİTİŞ ---


        ServerSocket SSOKET = null;
        try {
            SSOKET = new ServerSocket(PORT);
            SSOKET.setSoTimeout(TIMEOUT);
            System.out.println("Server başlatıldı, port:" + PORT);

            while (true) {
                try (Socket clientSocket = SSOKET.accept();
                     InputStream in = clientSocket.getInputStream();
                     BufferedReader reader = new BufferedReader(new InputStreamReader(in))) {

                    System.out.println("Client bağlandı: " + clientSocket.getInetAddress());
                    clientSocket.setSoTimeout(TIMEOUT);

                    String line;
                    while ((line = reader.readLine()) != null) {
                        System.out.println("Alınan veri: " + line);

                        // --- YENİ: Veriyi STM32'ye Gönder ---
                        // 'line' bir String. Java'da readLine() satır sonu karakterini ('\n')
                        // okumaz ama veriden atar. STM32'nin veriyi tam alması için 
                        // satır sonu karakterini (newline) ekleyerek göndermek iyi bir pratiktir.
                        String dataToSend = line + "\n";
                        byte[] bytesToSend = dataToSend.getBytes();
                        stm32Port.writeBytes(bytesToSend, bytesToSend.length);
                        System.out.println("Veri STM32'ye gönderildi.");
                        // --- YENİ BİTİŞ ---
                    }

                }
                System.out.println("Client bağlantısı sonlandı, yeni bağlantı bekleniyor...");
            }

        } catch (IOException e) {
            System.err.println("Server hatası: " + e.getMessage());
        } finally {
            if (SSOKET != null) {
                try {
                    SSOKET.close();
                } catch (IOException e) {
                    System.err.println("Server socket kapatılırken hata: " + e.getMessage());
                }
            }

            // --- YENİ: Seri Portu Kapat ---
            if (stm32Port.isOpen()) {
                stm32Port.closePort();
                System.out.println("Seri port kapatıldı.");
            }
            // --- YENİ BİTİŞ ---
        }
    }
}