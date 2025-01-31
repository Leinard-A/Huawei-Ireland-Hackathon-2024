def getKnown(mode):
    if mode == 'ls': # Latency Sensitivity
        return ['low', 
                'medium',
                'high']
    elif mode == 'timeStep':
        return 168
    elif mode == 'cpuTypes':
        return ['CPU.S1',
                'CPU.S2',
                'CPU.S3',
                'CPU.S4']
    elif mode == 'gpuTypes':
        return ['GPU.S1',
                'GPU.S2',
                'GPU.S3'
                ]
    elif mode == 'pt': # Processor types
        return ['CPU', 'GPU']