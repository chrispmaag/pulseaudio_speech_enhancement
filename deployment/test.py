from denoiser.enhance import enhance

enhance(model_path='./denoiser/best.th',
        noisy_dir='/tmp/', 
        file_location='./static/15ae60db-dacd-4f0f-aafb-20067420ed1d-noisy.wav',
        out_dir='./static/',
        noisy_json=None,
        sample_rate=16000,
        batch_size=1,
        device='cpu',
        num_workers=10,
        dns48=False,
        dns64=False,
        master64=False,
        dry=0,
        streaming=False,
        verbose=20)
