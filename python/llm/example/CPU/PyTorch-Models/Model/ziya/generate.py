#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import torch
import time
import argparse
import numpy as np

from transformers import AutoTokenizer


ZIYA_PROMPT_FORMAT = "<human>: \n{prompt}\n<bot>: \n"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict Tokens using `generate()` API for Ziya model')
    parser.add_argument('--repo-id-or-model-path', type=str, default="IDEA-CCNL/Ziya-Coding-34B-v1.0",
                        help='The huggingface repo id for the Ziya model to be downloaded'
                             ', or the path to the huggingface checkpoint folder')
    parser.add_argument('--prompt', type=str, default="def quick_sort(arr):\n",
                        help='Prompt to infer') 
    parser.add_argument('--n-predict', type=int, default=128,
                        help='Max tokens to predict')

    args = parser.parse_args()
    model_path = args.repo_id_or_model_path

    
    from transformers import AutoModelForCausalLM
    from bigdl.llm import optimize_model
    # enabling `use_cache=True` allows the model to utilize the previous
    # key/values attentions to speed up decoding;
    # to obtain optimal performance with BigDL-LLM `optimization_model` API optimizations,
    # it is important to set use_cache=True for Ziya models
    model = AutoModelForCausalLM.from_pretrained(model_path,
                                                 trust_remote_code=True,
                                                 use_cache=True)
    model = optimize_model(model)

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path,
                                              trust_remote_code=True)
    
    # Generate predicted tokens
    with torch.inference_mode():
        prompt = ZIYA_PROMPT_FORMAT.format(prompt=args.prompt)
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
 
        st = time.time()
        output = model.generate(input_ids,
                                max_new_tokens=args.n_predict,
                                do_sample = True,
                                top_p = 0.85,
                                temperature = 0.8,
                                repetition_penalty = 0.95,
                                eos_token_id = tokenizer.eos_token_id,
                                pad_token_id = tokenizer.pad_token_id,
                                )
        end = time.time()
        output_str = tokenizer.batch_decode(output)[0]
        print(f'Inference time: {end-st} s')
        print('-'*20, 'Prompt', '-'*20)
        print(prompt)
        print('-'*20, 'Output', '-'*20)
        print(output_str)
       