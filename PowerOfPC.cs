using System;
using System.Diagnostics;

namespace BotAICrypto
{
    class PowerOfPC
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Computational Power Analysis");

            // Get CPU usage
            var cpuUsage = GetCpuUsage();
            Console.WriteLine($"CPU Usage: {cpuUsage}%");

            // Get available memory
            var availableMemory = GetAvailableMemory();
            Console.WriteLine($"Available Memory: {availableMemory} MB");

            // Get disk usage
            var diskUsage = GetDiskUsage();
            Console.WriteLine($"Disk Usage: {diskUsage}%");

            // Get GPU usage (if available)
            var gpuUsage = GetGpuUsage();
            Console.WriteLine($"GPU Usage: {gpuUsage}%");
        }

        static double GetCpuUsage()
        {
            var cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
            cpuCounter.NextValue();
            System.Threading.Thread.Sleep(1000);
            return Math.Round(cpuCounter.NextValue(), 2);
        }

        static double GetAvailableMemory()
        {
            var memCounter = new PerformanceCounter("Memory", "Available MBytes");
            return Math.Round(memCounter.NextValue(), 2);
        }

        static double GetDiskUsage()
        {
            var diskCounter = new PerformanceCounter("LogicalDisk", "% Free Space", "_Total");
            return 100 - Math.Round(diskCounter.NextValue(), 2);
        }

        static double GetGpuUsage()
        {
            try
            {
                var gpuCounter = new PerformanceCounter("GPU Engine", "Utilization Percentage", "engtype_3D");
                return Math.Round(gpuCounter.NextValue(), 2);
            }
            catch (Exception)
            {
                return 0; // GPU usage not available
            }
        }
    }
}
