import multiprocessing as mp
import numpy as np
from tqdm import tqdm
def compute_score(rx, dual_codewords):
    scalar_products = np.sum(dual_codewords & rx, axis=1) % 2
    orthogonal_mask = (scalar_products == 0)
    orthogonal_vectors = dual_codewords[orthogonal_mask]
    score = np.sum(orthogonal_vectors, axis=0)
    return score
def run_simulation_batch(args):
    """Run a batch of simulations and return results"""
    batch_size, dual_codewords, err_num, main_iter_num, code_len, last_iter_num = args
    local_ker = 0
    local_wer = 0
    for _ in range(batch_size):
        # Create random error positions
        err_pos = np.random.choice(code_len, size=err_num, replace=False)
        err = np.zeros(code_len, dtype=bool)
        err[err_pos] = True
        rx = err.copy()
        decoded = False
        # decoding iterations
        for _ in range(main_iter_num):
            score = compute_score(rx, dual_codewords)
            min_pos = np.argmin(score)
            rx[min_pos] = ~rx[min_pos]  # Flip all positions with the minimum score
            if sum(rx) == 0:
                decoded = True
                break
        if last_iter_num  and not decoded:
            # Final decoding steps
            score = compute_score(rx, dual_codewords)
            min_k_indices = np.argpartition(score, last_iter_num)[:last_iter_num]
            rx[min_k_indices] = ~rx[min_k_indices]
        # Check if decoding was successful
        if not np.any(rx):
            local_ker += 1
        else:
            local_wer += 1
    return local_ker, local_wer
def main():
    # Parameters
    code_len = 127
    err_num = 12
    main_iter_num = 12  #err_num#5 * 2 ** 2
    last_iter_num = 0
    sim_num = 10000
    process_num = 100
    # Determine number of processes
    num_processes = min(mp.cpu_count(), process_num)
    print(f"Running on {num_processes} processes")
    # Load the dual_codewords matrix once
    print("Loading dual min codewords matrix...")
    #dual_codewords = np.load('dualdecvec.npy').astype(bool)
    dual_codewords = np.loadtxt('dualdecvec_nploadtxt.txt').astype(bool)
    # Calculate batch size per process
    batch_size = sim_num // num_processes
    remainder = sim_num % num_processes
    batches = [batch_size + 1 if i < remainder else batch_size for i in range(num_processes)]
    # Prepare arguments for each process
    args = [(batch, dual_codewords, err_num, main_iter_num, code_len, last_iter_num) for batch in batches]
    # Run simulations in parallel
    print(f"Running {sim_num} simulations in parallel...")
    with mp.Pool(processes=num_processes) as pool:
        results = list(tqdm(pool.imap(run_simulation_batch, args),
                            total=num_processes,
                            desc="Processing batches"))
    # Combine results
    wer = sum(result[1] for result in results)
    # Print results
    print(f'WER: {wer / sim_num :.8f}')
if __name__ == "__main__":
    main()
# results for main_iter_num == err_num and last_iter_num == 0:
# err=11 - 0.0018
# err=12 - 0.0983
# err=13 - 0.4771
# err=14 - 0.8322
# err=15 - 0.969
# err=16 - 0.994
