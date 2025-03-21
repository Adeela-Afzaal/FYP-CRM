using BlazorApp_Meta_UI.Models;

namespace BlazorApp_Meta_UI.Services
{
    public class ScheduleService
    {
        private List<ScheduledPost> scheduledPosts = new();
        private readonly Timer timer;

        public event Action OnScheduledPostsUpdated;
        public event Func<ScheduledPost, Task> OnPostPublish;

        public ScheduleService()
        {
            timer = new Timer(CheckScheduledPosts, null, TimeSpan.Zero, TimeSpan.FromMinutes(1));
        }

        public List<ScheduledPost> GetScheduledPosts() => scheduledPosts;

        public void AddScheduledPost(ScheduledPost post)
        {
            scheduledPosts.Add(post);
            OnScheduledPostsUpdated?.Invoke();
        }

        public void RemoveScheduledPost(ScheduledPost post)
        {
            scheduledPosts.Remove(post);
            OnScheduledPostsUpdated?.Invoke();
        }

        private async void CheckScheduledPosts(object state)
        {
            var now = DateTime.Now;

            var duePosts = scheduledPosts
                .Where(post => post.ScheduledDateTime <= now)
                .ToList();

            foreach (var post in duePosts)
            {
                if (OnPostPublish != null)
                {
                    await OnPostPublish.Invoke(post);
                }

                scheduledPosts.Remove(post);
            }

            if (duePosts.Any())
            {
                OnScheduledPostsUpdated?.Invoke();
            }
        }
    }
}
