"""Review: capacity planner for training runs. It said a 13B model fits with DDP on 80 GB GPUs; the job
OOMed at step 1. Find the bug, fix it, explain:

WHY:
"""


def bytes_per_param_mixed_adam():
    params_bf16 = 2
    grads_bf16 = 2
    master_fp32 = 4
    adam_states_fp32 = 8  # m and v, 4 bytes each
    return params_bf16 + grads_bf16 + master_fp32 + adam_states_fp32


def fits_ddp(n_params, gpu_bytes, activation_bytes):
    return n_params * bytes_per_param_mixed_adam() + activation_bytes <= gpu_bytes
