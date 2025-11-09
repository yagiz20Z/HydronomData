using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;
using System.Collections.Generic;

#region Data Classes

public class Root
{
    [JsonPropertyName("ts")]
    public string RootTimestamp { get; set; }

    [JsonPropertyName("source")]
    public string Source { get; set; }

    [JsonPropertyName("pose")]
    public Pose Pose { get; set; }

    [JsonPropertyName("obstacles_global")]
    public List<Obstacle> ObstaclesGlobal { get; set; }

    [JsonPropertyName("camera_objects_global")]
    public List<CameraObject> CameraObjectsGlobal { get; set; }
}

public class Pose
{
    [JsonPropertyName("ts")]
    public string PoseTimestamp { get; set; }

    [JsonPropertyName("source")]
    public string Source { get; set; }

    [JsonPropertyName("quality")]
    public string Quality { get; set; }

    [JsonPropertyName("utm")]
    public UTM UTM { get; set; }

    [JsonPropertyName("velocity")]
    public Velocity Velocity { get; set; }

    [JsonPropertyName("orientation")]
    public Orientation Orientation { get; set; }
}

public class UTM
{
    [JsonPropertyName("x")]
    public double X { get; set; }

    [JsonPropertyName("y")]
    public double Y { get; set; }

    [JsonPropertyName("alt")]
    public double Alt { get; set; }
}

public class Velocity
{
    [JsonPropertyName("vx")]
    public double Vx { get; set; }

    [JsonPropertyName("vy")]
    public double Vy { get; set; }

    [JsonPropertyName("speed_mps")]
    public double SpeedMps { get; set; }
}

public class Orientation
{
    [JsonPropertyName("z")]
    public double Z { get; set; }

    [JsonPropertyName("w")]
    public double W { get; set; }
}

public class Obstacle
{
    [JsonPropertyName("bearing_deg")]
    public double BearingDeg { get; set; }

    [JsonPropertyName("range_m")]
    public double RangeM { get; set; }

    [JsonPropertyName("w")]
    public double W { get; set; }

    [JsonPropertyName("l")]
    public double L { get; set; }

    [JsonPropertyName("x")]
    public double X { get; set; }

    [JsonPropertyName("y")]
    public double Y { get; set; }

    [JsonPropertyName("utm_x")]
    public double UtmX { get; set; }

    [JsonPropertyName("utm_y")]
    public double UtmY { get; set; }
}

public class CameraObject
{
    [JsonPropertyName("id")]
    public int Id { get; set; }

    [JsonPropertyName("label")]
    public string Label { get; set; }

    [JsonPropertyName("x")]
    public double X { get; set; }

    [JsonPropertyName("y")]
    public double Y { get; set; }

    [JsonPropertyName("confidence")]
    public double Confidence { get; set; }

    [JsonPropertyName("utm_x")]
    public double UtmX { get; set; }

    [JsonPropertyName("utm_y")]
    public double UtmY { get; set; }
}

#endregion

class TcpJsonClient
{
    private const string Host = "172.31.8.25"; // your server IP
    private const int Port = 5055;             // your server port

    public static async Task Main()
    {
        Console.WriteLine($"[CLIENT] Connecting to {Host}:{Port}...");

        try
        {
            using TcpClient client = new TcpClient();
            await client.ConnectAsync(Host, Port);
            Console.WriteLine("[CLIENT] Connected!");

            using NetworkStream stream = client.GetStream();
            using StreamReader reader = new StreamReader(stream, Encoding.UTF8);

            StringBuilder buffer = new StringBuilder();

            while (true)
            {
                char[] chunk = new char[4096];
                int bytesRead = await reader.ReadAsync(chunk, 0, chunk.Length);

                if (bytesRead == 0)
                {
                    Console.WriteLine("[CLIENT] Server disconnected.");
                    break;
                }

                buffer.Append(chunk, 0, bytesRead);

                // Parse multiple JSON objects if available
                bool foundOne = true;
                while (foundOne)
                {
                    foundOne = false;
                    string text = buffer.ToString();

                    int start = text.IndexOf('{');
                    int end = FindJsonEnd(text, start);

                    if (start != -1 && end != -1)
                    {
                        string json = text.Substring(start, end - start + 1);
                        buffer.Remove(0, end + 1);
                        foundOne = true;

                        try
                        {
                            var packet = JsonSerializer.Deserialize<Root>(json);
                            if (packet != null)
                                ProcessPacket(packet);
                        }
                        catch (JsonException ex)
                        {
                            // partial JSON, wait for next data
                            buffer.Insert(0, json);
                            break;
                        }
                    }
                }
            }
        }
        catch (SocketException ex)
        {
            Console.WriteLine($"[ERROR] Could not connect: {ex.Message}");
        }
    }

    // Robust method to find correct closing brace for a JSON object
    private static int FindJsonEnd(string text, int start)
    {
        if (start == -1) return -1;
        int depth = 0;
        for (int i = start; i < text.Length; i++)
        {
            if (text[i] == '{') depth++;
            else if (text[i] == '}')
            {
                depth--;
                if (depth == 0)
                    return i;
            }
        }
        return -1;
    }

    private static void ProcessPacket(Root data)
    {
        Console.WriteLine("\n--- New Packet ---");
        Console.WriteLine($"Root TS: {data.RootTimestamp}");
        Console.WriteLine($"Pose TS: {data.Pose?.PoseTimestamp}");
        Console.WriteLine($"Source: {data.Source}");

        if (data.Pose != null)
        {
            Console.WriteLine($"UTM: ({data.Pose.UTM.X:F3}, {data.Pose.UTM.Y:F3}, alt={data.Pose.UTM.Alt})");
            Console.WriteLine($"Velocity: vx={data.Pose.Velocity.Vx:F3}, vy={data.Pose.Velocity.Vy:F3}, speed={data.Pose.Velocity.SpeedMps:F2}");
            Console.WriteLine($"Orientation: z={data.Pose.Orientation.Z:F5}, w={data.Pose.Orientation.W:F5}");
        }

        if (data.ObstaclesGlobal != null)
        {
            Console.WriteLine($"Obstacles: {data.ObstaclesGlobal.Count}");
            foreach (var o in data.ObstaclesGlobal)
                Console.WriteLine($" - Bearing {o.BearingDeg:F1}°, Range {o.RangeM:F2}m, Pos=({o.X:F3},{o.Y:F3})");
        }

        if (data.CameraObjectsGlobal != null)
        {
            Console.WriteLine($"Camera Objects: {data.CameraObjectsGlobal.Count}");
            foreach (var c in data.CameraObjectsGlobal)
                Console.WriteLine($" - {c.Label} (ID={c.Id}, conf={c.Confidence:F2}) @ ({c.X:F2},{c.Y:F2})");
        }
    }
}
