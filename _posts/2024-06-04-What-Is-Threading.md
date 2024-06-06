---
layout: post
title: What is Threading?
---

When we're writing a program, we usually write things sequentially. Which, is great, but modern computers have more computing power and can do more. We can use different processes to concurrently solve problems to get a faster result. 

### Multithreading vs Multiprocessing
Multithreading is the ability for one *process* to run multiple threads. 
Multiprocessing is the ability for a *system* to run multiple processes. 

A system can have multiprocessing of multiple processes, where each process uses multithreading. 

#### Concurrency vs Parallelism
Multithreading is concurrent, which means that the threads don't actually run at the same time. They mimic running at the same time by staggering execution of a thread. Parallelism is what multiprocessing has, where processes do execute at the same time.

This is mainly because a process has its own memory and interpreter, whereas in multithreading, all threads share the same interpreter. 

### Python's Global Interpreter Lock
Python has something called a *Global Interpreter Lock*, it only allows one thread to have control of the Python interpreter. Only one thread can be executing at a time. Python works by using reference counting, meaning that when data is created in Python, Python tracks the amount of references the object has. When all references are deleted, the memory is freed. In order to prevent a race condition where multiple threads are trying to edit the reference counter, the GIL was introduced. 

This does not mean that you don't have to use a lock in your Python code. GIL only protects the interpreter. You still want consistency if you share state between threads. You don't know when your thread will get interrupted and switch to executing another thread, which means that when you save a state in a thread, you want to lock that code. 

### What is a Daemon thread?
A Daemon thread is one that runs without blocking the main program.

### Python Threading Coding Notes

#### What is the difference between lock() and join()?
Lock guarantees that only one thread can execute a portion of code at a time.
Join waits for a thread to complete. 

#### What is RLock?
RLock is a lock that can be acquired many times by the thread that got it the first time. The lock stays locked and is held until each acquisition is released. 

In a case where a locked function is calling another locked function, that code would not work with a normal lock. The lock would have to be released before the second function could be entered. If you have a RLock, the same thread can enter both functions. 

As of Python 3.2+, RLocks do not have any sigificantly greater performance cost than a regular Lock. 