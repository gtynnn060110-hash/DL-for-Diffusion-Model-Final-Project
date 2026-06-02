import math
from typing import Tuple

import torch
from torch import nn


def get_default_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


class SinusoidalTimeEmbedding(nn.Module):
    def __init__(self, embedding_dim: int) -> None:
        super().__init__()
        if embedding_dim <= 0 or embedding_dim % 2 != 0:
            raise ValueError("embedding_dim must be a positive even number.")
        self.embedding_dim = embedding_dim

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        if t.ndim == 2 and t.shape[-1] == 1:
            t = t.squeeze(-1)
        elif t.ndim != 1:
            raise ValueError("t must have shape (batch,) or (batch, 1).")

        half_dim = self.embedding_dim // 2
        freq = torch.arange(half_dim, device=t.device, dtype=t.dtype)
        freq = torch.exp(-math.log(10000.0) * freq / max(half_dim - 1, 1))
        angles = t.unsqueeze(-1) * freq.unsqueeze(0)
        return torch.cat([torch.sin(angles), torch.cos(angles)], dim=-1)


class RectifiedFlowMLP(nn.Module):
    def __init__(
        self,
        seq_len: int = 50,
        point_dim: int = 3,
        hidden_dim: int = 512,
        time_embedding_dim: int = 64,
        num_hidden_layers: int = 3,
    ) -> None:
        super().__init__()
        if seq_len <= 0 or point_dim <= 0:
            raise ValueError("seq_len and point_dim must be positive.")
        if hidden_dim <= 0 or num_hidden_layers <= 0:
            raise ValueError("hidden_dim and num_hidden_layers must be positive.")

        self.seq_len = seq_len
        self.point_dim = point_dim
        self.flat_dim = seq_len * point_dim
        self.time_embedding = SinusoidalTimeEmbedding(time_embedding_dim)

        layers = [
            nn.Linear(self.flat_dim + time_embedding_dim, hidden_dim),
            nn.SiLU(),
        ]
        for _ in range(num_hidden_layers - 1):
            layers.extend([nn.Linear(hidden_dim, hidden_dim), nn.SiLU()])
        layers.append(nn.Linear(hidden_dim, self.flat_dim))
        self.network = nn.Sequential(*layers)

    def _prepare_inputs(self, x: torch.Tensor, t: torch.Tensor) -> Tuple[torch.Tensor, bool]:
        if x.ndim == 3:
            if x.shape[1] != self.seq_len or x.shape[2] != self.point_dim:
                raise ValueError(
                    f"x shape must be (batch, {self.seq_len}, {self.point_dim}) "
                    f"or (batch, {self.flat_dim}). Got {tuple(x.shape)}."
                )
            x_flat = x.reshape(x.shape[0], self.flat_dim)
            should_reshape = True
        elif x.ndim == 2 and x.shape[1] == self.flat_dim:
            x_flat = x
            should_reshape = False
        else:
            raise ValueError(
                f"x shape must be (batch, {self.seq_len}, {self.point_dim}) "
                f"or (batch, {self.flat_dim}). Got {tuple(x.shape)}."
            )

        if t.ndim == 0:
            t = t.unsqueeze(0)
        if t.ndim == 1 and t.shape[0] == 1 and x_flat.shape[0] > 1:
            t = t.repeat(x_flat.shape[0])
        elif t.ndim == 2 and t.shape[0] == 1 and t.shape[1] == 1 and x_flat.shape[0] > 1:
            t = t.repeat(x_flat.shape[0], 1)

        if t.shape[0] != x_flat.shape[0]:
            raise ValueError(
                f"batch size mismatch between x and t: {x_flat.shape[0]} vs {t.shape[0]}."
            )

        t = t.to(device=x_flat.device, dtype=x_flat.dtype)
        return x_flat, should_reshape, t

    def forward(self, x: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        x_flat, should_reshape, t = self._prepare_inputs(x, t)
        t_embed = self.time_embedding(t)
        model_input = torch.cat([x_flat, t_embed], dim=-1)
        v = self.network(model_input)
        if should_reshape:
            return v.reshape(x_flat.shape[0], self.seq_len, self.point_dim)
        return v


def build_model(
    seq_len: int = 50,
    point_dim: int = 3,
    hidden_dim: int = 512,
    time_embedding_dim: int = 64,
    num_hidden_layers: int = 3,
    device: torch.device | None = None,
) -> RectifiedFlowMLP:
    model = RectifiedFlowMLP(
        seq_len=seq_len,
        point_dim=point_dim,
        hidden_dim=hidden_dim,
        time_embedding_dim=time_embedding_dim,
        num_hidden_layers=num_hidden_layers,
    )
    target_device = device if device is not None else get_default_device()
    return model.to(target_device, dtype=torch.float32)


class RectifiedFlowConditionalMLP(nn.Module):
    def __init__(
        self,
        seq_len: int = 50,
        point_dim: int = 3,
        condition_dim: int = 4,
        hidden_dim: int = 512,
        time_embedding_dim: int = 64,
        num_hidden_layers: int = 3,
    ) -> None:
        super().__init__()
        if seq_len <= 0 or point_dim <= 0:
            raise ValueError("seq_len and point_dim must be positive.")
        if condition_dim <= 0:
            raise ValueError("condition_dim must be positive.")
        if hidden_dim <= 0 or num_hidden_layers <= 0:
            raise ValueError("hidden_dim and num_hidden_layers must be positive.")

        self.seq_len = seq_len
        self.point_dim = point_dim
        self.flat_dim = seq_len * point_dim
        self.condition_dim = condition_dim
        self.time_embedding = SinusoidalTimeEmbedding(time_embedding_dim)

        layers = [
            nn.Linear(self.flat_dim + time_embedding_dim + condition_dim, hidden_dim),
            nn.SiLU(),
        ]
        for _ in range(num_hidden_layers - 1):
            layers.extend([nn.Linear(hidden_dim, hidden_dim), nn.SiLU()])
        layers.append(nn.Linear(hidden_dim, self.flat_dim))
        self.network = nn.Sequential(*layers)

    def _prepare_inputs(
        self,
        x: torch.Tensor,
        t: torch.Tensor,
        condition: torch.Tensor,
    ) -> Tuple[torch.Tensor, bool, torch.Tensor, torch.Tensor]:
        if x.ndim == 3:
            if x.shape[1] != self.seq_len or x.shape[2] != self.point_dim:
                raise ValueError(
                    f"x shape must be (batch, {self.seq_len}, {self.point_dim}) "
                    f"or (batch, {self.flat_dim}). Got {tuple(x.shape)}."
                )
            x_flat = x.reshape(x.shape[0], self.flat_dim)
            should_reshape = True
        elif x.ndim == 2 and x.shape[1] == self.flat_dim:
            x_flat = x
            should_reshape = False
        else:
            raise ValueError(
                f"x shape must be (batch, {self.seq_len}, {self.point_dim}) "
                f"or (batch, {self.flat_dim}). Got {tuple(x.shape)}."
            )

        if t.ndim == 0:
            t = t.unsqueeze(0)
        if t.ndim == 1 and t.shape[0] == 1 and x_flat.shape[0] > 1:
            t = t.repeat(x_flat.shape[0])
        elif t.ndim == 2 and t.shape[0] == 1 and t.shape[1] == 1 and x_flat.shape[0] > 1:
            t = t.repeat(x_flat.shape[0], 1)
        if t.shape[0] != x_flat.shape[0]:
            raise ValueError(
                f"batch size mismatch between x and t: {x_flat.shape[0]} vs {t.shape[0]}."
            )

        if condition.ndim == 1:
            condition = condition.view(1, -1)
        if condition.ndim != 2 or condition.shape[1] != self.condition_dim:
            raise ValueError(
                f"condition must have shape (batch, {self.condition_dim}) "
                f"or ({self.condition_dim},). Got {tuple(condition.shape)}."
            )
        if condition.shape[0] == 1 and x_flat.shape[0] > 1:
            condition = condition.repeat(x_flat.shape[0], 1)
        if condition.shape[0] != x_flat.shape[0]:
            raise ValueError(
                "batch size mismatch between x and condition: "
                f"{x_flat.shape[0]} vs {condition.shape[0]}."
            )

        t = t.to(device=x_flat.device, dtype=x_flat.dtype)
        condition = condition.to(device=x_flat.device, dtype=x_flat.dtype)
        return x_flat, should_reshape, t, condition

    def forward(self, x: torch.Tensor, t: torch.Tensor, condition: torch.Tensor) -> torch.Tensor:
        x_flat, should_reshape, t, condition = self._prepare_inputs(x, t, condition)
        t_embed = self.time_embedding(t)
        model_input = torch.cat([x_flat, t_embed, condition], dim=-1)
        v = self.network(model_input)
        if should_reshape:
            return v.reshape(x_flat.shape[0], self.seq_len, self.point_dim)
        return v


def build_conditional_model(
    seq_len: int = 50,
    point_dim: int = 3,
    condition_dim: int = 4,
    hidden_dim: int = 512,
    time_embedding_dim: int = 64,
    num_hidden_layers: int = 3,
    device: torch.device | None = None,
) -> RectifiedFlowConditionalMLP:
    model = RectifiedFlowConditionalMLP(
        seq_len=seq_len,
        point_dim=point_dim,
        condition_dim=condition_dim,
        hidden_dim=hidden_dim,
        time_embedding_dim=time_embedding_dim,
        num_hidden_layers=num_hidden_layers,
    )
    target_device = device if device is not None else get_default_device()
    return model.to(target_device, dtype=torch.float32)
