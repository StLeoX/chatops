let workflow = {
  apiVersion: "chaos-mesh.org/v1alpha1",
  kind: "Workflow",
  metadata: { name: "workflow-1s1s1s", namespace: "sock-shop" },
  spec: {
    entry: "paraller-490912",
    templates: [
      {
        name: "paraller-490912",
        templateType: "Parallel",
        children: ["fault-18c36a2d", "fault-bc93c7c9", "fault-3da791f4"],
        deadline: "10h",
      },
      {
        name: "fault-18c36a2d",
        templateType: "FaultConfig",
        deadline: "1h",
        list: [
          {
            type: "Inject",
            chaosType: "NetworkChaos",
            NetworkChaos: {
              mode: "all",
              selector: {
                namespaces: ["sock-shop"],
                labelSelectors: { name: "user" },
              },
              action: "delay",
              delay: {
                latency: "500ms",
                jitter: "500ms",
                correlation: "50",
                direction: "to",
              },
            },
          },
          { type: "Wait", deadline: "300s" },
          { index: 0, type: "Recover" },
        ],
      },
      {
        name: "fault-bc93c7c9",
        templateType: "FaultConfig",
        deadline: "1h",
        list: [
          {
            type: "Inject",
            chaosType: "NetworkChaos",
            NetworkChaos: {
              mode: "all",
              selector: {
                namespaces: ["sock-shop"],
                labelSelectors: { name: "front-end" },
              },
              action: "delay",
              delay: {
                latency: "500ms",
                jitter: "500ms",
                correlation: "50",
                direction: "to",
              },
            },
          },
          { type: "Wait", deadline: "300s" },
          { index: 0, type: "Recover" },
        ],
      },
      {
        name: "fault-3da791f4",
        templateType: "FaultConfig",
        deadline: "1h",
        list: [
          {
            type: "Inject",
            chaosType: "NetworkChaos",
            NetworkChaos: {
              mode: "all",
              selector: {
                namespaces: ["sock-shop"],
                labelSelectors: { name: "catalogue" },
              },
              action: "delay",
              delay: {
                latency: "500ms",
                jitter: "500ms",
                correlation: "50",
                direction: "to",
              },
            },
          },
          { type: "Wait", deadline: "300s" },
          { index: 0, type: "Recover" },
        ],
      },
    ],
  },
};
