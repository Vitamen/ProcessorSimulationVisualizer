from django.template import Context, loader
from django.http import HttpResponse
from experimentManager.models import *

def index(request):
    t = loader.get_template('metrics/metrics.html')
    metric_objects = Metric.objects.all()
    metrics = []
    for metric_object in metric_objects:
        metric_item = {"metricname" : metric_object.metricname, 
                       "metrictype" : metric_object.metrictype }
        metrics.append(metric_item)
    c = Context({
                 "metrics": metrics
    })
    return HttpResponse(t.render(c))

def getMetricsOfTypeForExperiments(request):
    experiments = request.POST.getlist('experiments')
    metric_type = request.POST.get('metric_type');
    metric_objects = Metric.objects.filter(metrictype='HISTOGRAM')
    metrics = []
    for metric_object in metric_objects:
        metrics.append(metric_object.metricname)
    if len(experiments) == 0 :
        metrics = []
    c = Context({
        'metrics': metrics
    })
    return HttpResponse(c)

def updateMetricType(request):
    metric_id = request.POST.get('metric_id')
    metric_type = request.POST.get('metric_type')
    metrics = Metric.objects.filter(metricname=metric_id)
    for metric in metrics:
        metric.metrictype = metric_type
        metric.save()
    return HttpResponse({}) 

def setUpMetrics(request):
    metrics = Metric.objects.all()
    for metric in metrics:
        metric.delete()
    metrics = [
               "cycles",
                "core_insn_fetched",
                "core_insn_fetched_onpath",
                "core_insn_retired",
                "core_macroinsn_retired",
                "core_bp_all",
                "core_bp_all_misp",
                "core_bp_jmp",
                "core_bp_jmp_misp",
                "core_bp_cond",
                "core_bp_cond_misp",
                "core_bp_call",
                "core_bp_call_misp",
                "core_bp_ret",
                "core_bp_ret_misp",
                "core_bp_indir",
                "core_bp_indir_misp",
                "core_rob_full",
                "core_full_window_stall",
                "core_full_window_stall_dc_miss",
                "core_full_window_stall_l2_miss",
                "core_retire_normal",
                "core_flush",
                "fetch_stalled",
                "fetch_blocked_icache",
                "fetch_blocked_serialize",
                "icache_access",
                "icache_hit",
                "icache_miss",
                "decode_stalled",
                "map_stalled",
                "dcache_access",
                "dcache_access_ld",
                "dcache_access_st",
                "dcache_access_pre",
                "dcache_hit",
                "dcache_hit_upgr",
                "dcache_miss",
                "dcache_miss_upgr",
                "dcache_miss_np",
                "dcache_merge_mshr",
                "dcache_unique_miss",
                "dcache_wb",
                "l2_access",
                "l2_hit",
                "l2_miss",
                "l2_secondmiss",
                "l2_wb",
                "l2_mshrs",
                "dram_access",
                "dram_write",
                "exec",
                "nuke",
               ]

    for metric in metrics:
        Metric.objects.create(metricname=metric, metrictype='HISTOGRAM')
    c = Context({
    })
    return HttpResponse(c)