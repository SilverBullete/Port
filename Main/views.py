from django.shortcuts import render
from django.http import HttpResponse
from .ports import CloudController, WaterController, TreeController, LandsideController


# Create your views here.
def cloudController(request):
    # 接收post的文件
    img = request.FILES.get('img')
    # 定义上传文件保存的路径
    fname = 'Main/images/%s' % (img.name)
    # 将上传文件保存到静态目录下
    with open(fname, 'wb') as pic:
        for c in img.chunks():
            pic.write(c)
    # 接收post的阈值和波段序号
    threshold = request.POST.getlist("threshold")[0]
    band = request.POST.getlist("band")[0]
    # 接收云检测接口的响应结果
    response = CloudController(img.name, eval(threshold), eval(band))
    # 返回响应结果
    return HttpResponse(response)


def waterController(request):
    # 接收post的阈值文件名和波段序号
    threshold = request.POST.getlist("threshold")[0]
    fname = request.POST.getlist("fname")[0]
    band_green = request.POST.getlist("band_green")[0]
    band_nir = request.POST.getlist("band_nir")[0]
    # 接收水体检测接口的响应结果
    response = WaterController(fname, eval(threshold), eval(band_green), eval(band_nir))
    # 返回响应结果
    return HttpResponse(response)


def treeController(request):
    # 接收post的文件名和波段序号
    fname = request.POST.getlist("fname")[0]
    band_nir = request.POST.getlist("band_nir")[0]
    band_red = request.POST.getlist("band_red")[0]
    # 接收植被检测接口的响应结果
    response = TreeController(fname, eval(band_nir), eval(band_red))
    # 返回响应结果
    return HttpResponse(response)


def landsideController(request):
    # 接收post的文件名和阈值
    threshold = request.POST.getlist("threshold")[0]
    fname = request.POST.getlist("fname")[0]
    # 接收滑坡检测的响应结果
    response = LandsideController(fname, eval(threshold))
    # 返回响应结果
    return HttpResponse(response)
