from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "notes", "completed"]
        labels = {"title": "任务标题", "notes": "备注", "completed": "已完成"}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "例如：整理课程笔记"}),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "补充说明（可选）"}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("标题不能为空")
        return title
