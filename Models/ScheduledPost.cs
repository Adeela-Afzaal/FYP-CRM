using Microsoft.AspNetCore.Components.Forms;
using System;
using System.Collections.Generic;

namespace BlazorApp_Meta_UI.Models
{
    public class ScheduledPost
    {
       
        public DateTime ScheduledDateTime { get; set; }
        public string PostText { get; set; } = string.Empty;
        public List<IBrowserFile> SelectedFiles { get; set; } = new();
    }
}
