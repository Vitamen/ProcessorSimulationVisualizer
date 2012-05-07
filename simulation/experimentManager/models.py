from django.db import models
from datetime import datetime

# Create your models here.
class BenchmarkSuite(models.Model):
    suite = models.CharField(max_length=200, primary_key=True)
    def __unicode__(self):
        return self.suite

class Benchmarks(models.Model):
    suite = models.ForeignKey(BenchmarkSuite)
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

class Arguments(models.Model):
    argname = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    def __unicode__(self):
        return self.argname

class ArgumentSet(models.Model):
    setname = models.CharField(max_length=200, primary_key=True)
    def __unicode__(self):
        return self.setname

class ArgMembership(models.Model):
    setname = models.ForeignKey(ArgumentSet)
    argname = models.ForeignKey(Arguments)
    
class Experiments(models.Model):
    expname = models.CharField(max_length=200, primary_key=True)
    execpath = models.CharField(max_length=200, default="", null=True, blank=True)
    bsuite = models.ForeignKey(BenchmarkSuite, default=None, null=True, blank=True)
    argset = models.ForeignKey(ArgumentSet, default=None, null=True, blank=True)
    subdate = models.DateTimeField('submission date', default=None, blank=True, null=True)

def findOrCreateExperimentByName(expName):
    benchmarkSuite, created = BenchmarkSuite.objects.get_or_create(suite="suite")
    argumentSet, created = ArgumentSet.objects.get_or_create(setname="setname")
    experiments = Experiments.objects.filter(expname=expName);
    if len(experiments) == 1:
        return experiments[0]
    elif len(experiments) == 0:
        experiment = Experiments.objects.create(expname=expName, execpath="", bsuite=benchmarkSuite, argset=argumentSet, subdate=datetime.now())
        return experiment
    else:
        print "ERROR: duplicate"
        return None

    
class ExperimentBenchmark(models.Model):
    expname = models.ForeignKey(Experiments)
    bmname = models.ForeignKey(Benchmarks)
   
METRIC_CHART_TYPE = (
               (u'000', u'HISTOGRAM'),
               (u'001', u'SCATTERPLOT'),
               (u'002', u'NOPLOT')
               )
class Metric(models.Model):
    metricname = models.CharField(max_length=200, primary_key=True)
    metrictype = models.CharField(max_length=2, choices=METRIC_CHART_TYPE)

def findOrCreateMetricByName(metricName):
    metrics = Metric.objects.filter(metricname=metricName);
    if len(metrics) == 1:
        return metrics[0]
    elif len(metrics) == 0:
        metric = Metric.objects.create(metricname=metricName, metrictype='HISTOGRAM')
        return metric
    else:
        print "ERROR: duplicate"
        return None

class ExperimentMetric(models.Model):
    expname = models.ForeignKey(Experiments)
    metricname = models.ForeignKey(Metric)