from django.db import models

# Create your models here.
class BenchmarkSuite(models.Model):
    suite = models.CharField(max_length=200, primary_key=True)
    def __unicode__(self):
        return self.suite

class Benchmarks(models.Model):
    suite = models.ForeignKey(BenchmarkSuite)
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

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
    execpath = models.CharField(max_length=200)
    bsuite = models.ForeignKey(BenchmarkSuite)
    argset = models.ForeignKey(ArgumentSet)
    subdate = models.DateTimeField('submission date')
    
class BenchmarkSet(models.Model):
    expname = models.ForeignKey(Experiments)
    bmarks = models.ForeignKey(Benchmarks)
    

