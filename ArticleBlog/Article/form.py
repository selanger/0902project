from django import forms

class UserForm(forms.Form):
    name = forms.CharField(max_length=32,required=True,label="账号")
    password = forms.CharField(max_length=8,min_length=6,label="密码")

    def clean_name(self):
        """"""
        ## 获取用户名
        name = self.cleaned_data.get("name")
        ## 校验规则  name 不能为   admin@126.com
        if name == "admin@126.com":
            ## 不允许
            self.add_error("name","不能为admin@126.com")
            self.add_error("name","不能为admin@126.com")
        else:
            #  允许
            return name


