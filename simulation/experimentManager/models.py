from django.db import models
from django import forms
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class BenchmarkSuite(models.Model):
    suite = models.CharField(max_length=200, primary_key=True)
    def __unicode__(self):
        return self.suite

class Benchmarks(models.Model):
    suite = models.ForeignKey(BenchmarkSuite, default=None, blank=True, null=True)
    name = models.CharField(max_length=200, primary_key=True)
    def __unicode__(self):
        return self.name

def findOrCreateBenchmarkByName(benchmarkName):
    benchmarks = Benchmarks.objects.filter(name=benchmarkName);
    if len(benchmarks) == 1:
        return benchmarks[0]
    elif len(benchmarks) == 0:
        benchmarkSuite, created = BenchmarkSuite.objects.get_or_create(suite="suite")
        benchmark = Benchmarks.objects.create(name=benchmarkName, suite=benchmarkSuite)
        return benchmark
    else:
        print "ERROR: duplicate"
        return None

class BinRevForms(forms.Form):
    binFile = forms.Field(widget=forms.FileInput, required=False)
    
class Experiments(models.Model):
    submissionName = models.CharField(max_length=200)
    subdate = models.DateTimeField('submission date', default=None, blank=True, null=True)
    expName = models.CharField(max_length=200)
    binrev = models.CharField(max_length=200, default="", null=True, blank=True)
    bsuite = models.ForeignKey(BenchmarkSuite, default=None, null=True, blank=True)
    exclBench = models.ManyToManyField(Benchmarks, default=None, null=True, blank=True)
    argset = models.CharField(max_length=1000)
    rootDirectory = models.CharField(max_length=1024)

class BaseExperiment(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=1000)

class ExtExperiment(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=1000)
    
class ExperimentBenchmark(models.Model):
    expName = models.ForeignKey(Experiments)
    benchmark = models.ForeignKey(Benchmarks)
   
METRIC_CHART_TYPE = (
               (u'000', u'HISTOGRAM'),
               (u'001', u'SCATTERPLOT'),
               (u'002', u'NOPLOT')
               )
class Metric(models.Model):
    metricname = models.CharField(max_length=200, primary_key=True)
    metrictype = models.CharField(max_length=2, choices=METRIC_CHART_TYPE, default="NO_PLOT")
    isAggregate = models.BooleanField(default=False)

def findOrCreateMetricByName(metricName, aggregate = False):
    metrics = Metric.objects.filter(metricname=metricName);
    if len(metrics) == 1:
        return metrics[0]
    elif len(metrics) == 0:
        metric = Metric.objects.create(metricname=metricName, metrictype='HISTOGRAM', isAggregate = aggregate)
        return metric
    else:
        print "ERROR: duplicate"
        return None
    
class MetricAggregate(models.Model):
    metric = models.ForeignKey(Metric)
    evalString = models.CharField(max_length=512)
        
class ExperimentMetric(models.Model):
    expname = models.ForeignKey(Experiments)
    metricname = models.ForeignKey(Metric)

class DefaultValues(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=1000)
