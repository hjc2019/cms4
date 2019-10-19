from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class logincheck(MiddlewareMixin):
    '''
    后端登录验证
    '''
    def process_request(self,request):
        '''
        :param request: 前端发送的请求
        :return:
        '''
        path = request.path
        if path.startswith("/cmsadmain") and not path == "/cmsadmain/login/":
            if request.session.get("user"):
                pass
            else:
                if path == "/cmsadmain/loginHandler/" and request.POST.get("username") == None:
                    return redirect("/cmsadmain/login/")
                else:
                    pass
                if path != "/cmsadmain/loginHandler/":
                    return redirect("/cmsadmain/login/")
