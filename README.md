[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/YFgwt0yY)
# MiniTorch Module 2

<img src="https://minitorch.github.io/minitorch.svg" width="50%">


* Docs: https://minitorch.github.io/

* Overview: https://minitorch.github.io/module2/module2/

This assignment requires the following files from the previous assignments. You can get these by running

```bash
python sync_previous_module.py previous-module-dir current-module-dir
```

The files that will be synced are:

        minitorch/operators.py minitorch/module.py minitorch/autodiff.py minitorch/scalar.py minitorch/scalar_functions.py minitorch/module.py project/run_manual.py project/run_scalar.py project/datasets.py

## Dataset 1 (Linear) Results
Number of points: 50
Size of hidden layer: 2
Learning rate: 0.1
Number of epochs: 500

Time per epoch: 0.031s

### Training logs:
Epoch: 0/500, loss: 0, correct: 0
Epoch: 10/500, loss: 34.221584629927825, correct: 33
Epoch: 20/500, loss: 33.516706758323224, correct: 32
Epoch: 30/500, loss: 33.10960056212826, correct: 32
Epoch: 40/500, loss: 32.859795691411456, correct: 32
Epoch: 50/500, loss: 32.69393421529645, correct: 32
Epoch: 60/500, loss: 32.57224216002464, correct: 32
Epoch: 70/500, loss: 32.47229373593878, correct: 32
Epoch: 80/500, loss: 32.380750977723004, correct: 32
Epoch: 90/500, loss: 32.289009717131535, correct: 32
Epoch: 100/500, loss: 32.190821821063714, correct: 32
Epoch: 110/500, loss: 32.080932889380264, correct: 32
Epoch: 120/500, loss: 31.95424102114362, correct: 32
Epoch: 130/500, loss: 31.805214817263927, correct: 32
Epoch: 140/500, loss: 31.627427496782943, correct: 32
Epoch: 150/500, loss: 31.413125512197652, correct: 32
Epoch: 160/500, loss: 31.152781648293622, correct: 32
Epoch: 170/500, loss: 30.83459721816307, correct: 32
Epoch: 180/500, loss: 30.443922299290378, correct: 32
Epoch: 190/500, loss: 29.96256509153825, correct: 32
Epoch: 200/500, loss: 29.367983258729534, correct: 33
Epoch: 210/500, loss: 28.63933381064067, correct: 35
Epoch: 220/500, loss: 27.7687155290238, correct: 39
Epoch: 230/500, loss: 26.73562485826192, correct: 41
Epoch: 240/500, loss: 25.516575580800534, correct: 44
Epoch: 250/500, loss: 24.124645965562472, correct: 46
Epoch: 260/500, loss: 22.59768036908909, correct: 46
Epoch: 270/500, loss: 20.94499668364835, correct: 46
Epoch: 280/500, loss: 19.262661178943933, correct: 48
Epoch: 290/500, loss: 17.588955736005396, correct: 48
Epoch: 300/500, loss: 16.03743315644638, correct: 48
Epoch: 310/500, loss: 14.633863325254806, correct: 49
Epoch: 320/500, loss: 13.413939795334292, correct: 49
Epoch: 330/500, loss: 12.332368756857433, correct: 49
Epoch: 340/500, loss: 11.356059943873769, correct: 49
Epoch: 350/500, loss: 10.50968032347512, correct: 49
Epoch: 360/500, loss: 9.77481111335794, correct: 49
Epoch: 370/500, loss: 9.147630599555503, correct: 49
Epoch: 380/500, loss: 8.587606983806394, correct: 50
Epoch: 390/500, loss: 8.08658445019968, correct: 50
Epoch: 400/500, loss: 7.6373074024553125, correct: 50
Epoch: 410/500, loss: 7.243055026411691, correct: 50
Epoch: 420/500, loss: 6.897704120605102, correct: 50
Epoch: 430/500, loss: 6.584065875582612, correct: 50
Epoch: 440/500, loss: 6.2979171329310395, correct: 50
Epoch: 450/500, loss: 6.03970497658056, correct: 50
Epoch: 460/500, loss: 5.803291826588424, correct: 50
Epoch: 470/500, loss: 5.584757196918464, correct: 50
Epoch: 480/500, loss: 5.380803789302544, correct: 50
Epoch: 490/500, loss: 5.189992168855156, correct: 50
Epoch: 500/500, loss: 5.011093332307256, correct: 50

### Training Visualizations

![Dataset 1 Decision Boundary](linear.png)
*Figure 1: Decision boundary for Linear Dataset*

![Dataset 1 Loss Graph](linear_loss.png)
*Figure 2: Loss graph for Diag Dataset*