from django import forms
from .models import Jasoseol, Comment

class JssForm(forms.ModelForm):
    class Meta:
        model = Jasoseol
        # updated_date 는 자동입력이기 때문에 사용자 입력 폼에 넣을 필요 x
        fields = ('title', 'content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # label은 각 필드 입력 제목
        self.fields['title'].label = "제목"
        self.fields['content'].label = "자기소개서 내용"
        self.fields['title'].widget.attrs.update({
            'class' : 'jss_title',
            'placeholder' : '제목',
        })
        self.fields['content'].widget.attrs.update({
            'class' : 'jss_content_form',
        })

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', )