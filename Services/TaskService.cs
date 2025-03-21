using System;
using System.Collections.Generic;

namespace BlazorApp_Meta_UI.Services
{
    public class TaskService
    {
        private Dictionary<DateTime, List<TaskItem>> tasks = new();

        // Event for task updates
        public event Action OnTasksUpdated;

        // Method to get tasks for a specific date
        public List<TaskItem> GetTasks(DateTime date)
        {
            var normalizedDate = date.Date; // Remove the time part
            return tasks.ContainsKey(normalizedDate) ? tasks[normalizedDate] : new List<TaskItem>();
        }

        // Method to add a task
        public void AddTask(DateTime date, string taskName, string priority)
        {
            var normalizedDate = date.Date;  // Ensure the date is correctly passed and set
            if (!tasks.ContainsKey(normalizedDate))
            {
                tasks[normalizedDate] = new List<TaskItem>();
            }
            tasks[normalizedDate].Add(new TaskItem { Name = taskName, Priority = priority, Date = normalizedDate });  // Set the date
            OnTasksUpdated?.Invoke();
        }


        // Method to remove a task
        public void RemoveTask(DateTime date, TaskItem task)
        {
            var normalizedDate = date.Date;
            if (tasks.ContainsKey(normalizedDate))
            {
                tasks[normalizedDate].Remove(task);
                if (tasks[normalizedDate].Count == 0)
                {
                    tasks.Remove(normalizedDate);
                }
            }
            OnTasksUpdated?.Invoke();
        }

        public List<TaskItem> GetAllTasks()
        {
            return tasks.SelectMany(t => t.Value).ToList();
        }

        // TaskItem class defined inside TaskService
        public class TaskItem
        {
            public string Name { get; set; } = string.Empty;
            public string Priority { get; set; } = "Low";

            public DateTime Date { get; set; } // Add the Date property to represent the task date

        }
    }
}
