using System;
using System.Diagnostics;
using System.Management;

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

            // Get total memory
            var totalMemory = GetTotalMemory();
            Console.WriteLine($"Total Memory: {totalMemory} MB");

            // Get disk usage
            var diskUsage = GetDiskUsage();
            Console.WriteLine($"Disk Usage: {diskUsage}%");

            // Get GPU usage (if available)
            var gpuUsage = GetGpuUsage();
            Console.WriteLine($"GPU Usage: {gpuUsage}%");

            // Get system uptime
            var uptime = GetSystemUptime();
            Console.WriteLine($"System Uptime: {uptime}");
        }

        static double GetCpuUsage()
        {
            try
            {
                var cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
                cpuCounter.NextValue();
                System.Threading.Thread.Sleep(1000);
                return Math.Round(cpuCounter.NextValue(), 2);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error getting CPU usage: {ex.Message}");
                return 0;
            }
        }

        static double GetAvailableMemory()
        {
            try
            {
                var memCounter = new PerformanceCounter("Memory", "Available MBytes");
                return Math.Round(memCounter.NextValue(), 2);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error getting available memory: {ex.Message}");
                return 0;
            }
        }

        static double GetTotalMemory()
        {
            try
            {
                var searcher = new ManagementObjectSearcher("SELECT Capacity FROM Win32_PhysicalMemory");
                double totalMemory = 0;
                foreach (var obj in searcher.Get())
                {
                    totalMemory += Convert.ToDouble(obj["Capacity"]);
                }
                return Math.Round(totalMemory / (1024 * 1024), 2); // Convert bytes to MB
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error getting total memory: {ex.Message}");
                return 0;
            }
        }

        static double GetDiskUsage()
        {
            try
            {
                var diskCounter = new PerformanceCounter("LogicalDisk", "% Free Space", "_Total");
                return 100 - Math.Round(diskCounter.NextValue(), 2);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error getting disk usage: {ex.Message}");
                return 0;
            }
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

        static string GetSystemUptime()
        {
            try
            {
                var uptime = TimeSpan.FromMilliseconds(Environment.TickCount64);
                return $"{uptime.Days} days, {uptime.Hours} hours, {uptime.Minutes} minutes";
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error getting system uptime: {ex.Message}");
                return "N/A";
            }
        }
    }
}
