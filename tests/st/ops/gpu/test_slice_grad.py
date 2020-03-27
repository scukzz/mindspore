# Copyright 2019 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

import pytest
from mindspore import Tensor
from mindspore.ops import operations as P
from mindspore.ops.operations import _grad_ops as G
import mindspore.nn as nn
from mindspore.common.api import ms_function
import numpy as np
import mindspore.context as context

context.set_context(device_target='GPU')


class SliceGrad(nn.Cell):
    def __init__(self):
        super(SliceGrad, self).__init__()

        self.slicegrad = G.SliceGrad()

    @ms_function
    def construct(self, dy, x):
        return self.slicegrad(dy, x, (0, 1, 0), (2, 1, 3))


@pytest.mark.level0
@pytest.mark.platform_x86_gpu_training
@pytest.mark.env_onecard
def test_slice():
    x = Tensor(np.array([[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]], [[5, 5, 5], [6, 6, 6]]]).astype(np.float32))
    dy = Tensor(np.array([[[3., 1., 2.]], [[4., 1., 4.]]]).astype(np.float32))
    slicegrad = SliceGrad()
    output = slicegrad(dy, x)
    expect = [[[0., 0., 0.],
               [3., 1., 2.]],
              [[0., 0., 0.],
               [4., 1., 4.]],
              [[0., 0., 0.],
               [0., 0., 0.]]]
    print(output)
    assert (output.asnumpy() == expect).all()